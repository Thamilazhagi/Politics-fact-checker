import os
import datetime
import sys
import yt_dlp
from google import genai

# --- 1. YOUR CONFIGURATION ---
# Put a real YouTube link here! (Keep it under 10 minutes for your first test)
TARGET_VIDEO_URL = "https://youtube.com/shorts/U5FOK4sin58?si=i0F9cLGLTzqKkr8-"

SYSTEM_PROMPT = """
You are a political analyst and dialogue editor specializing in Tamil Nadu politics.
Listen to this audio. Identify the speakers based on their voices (e.g., Reporter, Vijay, Udhayanidhi, Seeman, etc. or Speaker A/B if unknown).
Translate and write out the dialogue continuously in English. Skip filler words.
Whenever a political or factual claim is made, insert a fact-check immediately after.

Format exactly like this:
Reporter: [Question asked...]
Vijay: [Answer...]
(Verdict: FALSE / VERIFIED / MISLEADING / UNVERIFIED
What actually happened: [The reality based on TN political history/data]
Source: [What public record proves this])
"""

def extract_audio(video_url):
    print(f"📥 Downloading audio from: {video_url}")
    options = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])
    return "temp_audio.mp3"

def run_scavenger():
    print("🛰️ Waking up Cloud Scavenger...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: API Key missing.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    try:
        # Step 1: Rip the Audio
        audio_file = extract_audio(TARGET_VIDEO_URL)
        
        # Step 2: Upload to Gemini (Zero local CPU processing required!)
        print("🧠 Uploading audio to Gemini 2.5 Flash...")
        uploaded_audio = client.files.upload(file=audio_file)
        
        # Step 3: Analyze
        print("🔍 Analyzing dialogue and fact-checking claims (this takes a minute)...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[SYSTEM_PROMPT, uploaded_audio]
        )
        
        # Step 4: Save Report
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"reports/fact_check_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# 🛰️ Fact-Check Report\n\n**Source Video**: {TARGET_VIDEO_URL}\n**Date Analyzed**: {timestamp}\n\n---\n\n")
            f.write(response.text)
            
        print(f"🎉 SUCCESS! Report saved to {filename}")
        
        # Cleanup server files
        os.remove(audio_file)
        client.files.delete(name=uploaded_audio.name)
        
    except Exception as e:
        print(f"❌ PIPELINE FAILED: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_scavenger()
    
