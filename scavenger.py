import os
import datetime
import sys
import yt_dlp
from google import genai
from google.genai import types

# --- 1. YOUR CONFIGURATION ---
TARGET_VIDEO_URL = "https://youtube.com/shorts/U5FOK4sin58"

# We update the prompt to FORCE deep, multi-layered thinking and web searching
SYSTEM_PROMPT = """
You are an elite, obsessive political analyst and fact-checker specializing in Tamil Nadu politics.
Your instructions:
1. THINK DEEPLY 10 TIMES before you write a verdict. Do not take statements at face value.
2. ALWAYS USE GOOGLE SEARCH to ground your facts. Look up the exact political context, date, and who the speaker is defending or attacking.
3. Identify the speakers based on their voices.
4. Translate and write out the dialogue continuously in English.
5. Whenever a claim is made (even rhetorical defenses of a government), insert a brutal, logically sound fact-check.

Format exactly like this:
Speaker Name: [English translated dialogue]
(Verdict: FALSE / VERIFIED / MISLEADING / UNVERIFIED
Verification Analysis: [Deep analysis using real TN political context pulled from the web]
Source: [What public record/news proves this])
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
    print("🛰️ Waking up Cloud Scavenger (Ultra-Reasoning Mode)...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: API Key missing.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    try:
        audio_file = extract_audio(TARGET_VIDEO_URL)
        
        print("🧠 Uploading audio to Gemini 2.5 Pro...")
        uploaded_audio = client.files.upload(file=audio_file)
        
        print("🔍 Searching the web, analyzing dialogue, and deep-thinking (this will take 2-3 minutes)...")
        
        # THIS IS THE MAGIC: We force the Pro model to use Google Search Grounding natively
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[SYSTEM_PROMPT, uploaded_audio],
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}], # Enables live web-searching!
                temperature=0.2 # Keeps the AI cold, logical, and analytical
            )
        )
        
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"reports/fact_check_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# 🛰️ Fact-Check Report\n\n**Source Video**: {TARGET_VIDEO_URL}\n**Date Analyzed**: {timestamp}\n\n---\n\n")
            f.write(response.text)
            
        print(f"🎉 SUCCESS! Grounded report saved to {filename}")
        
        os.remove(audio_file)
        client.files.delete(name=uploaded_audio.name)
        
    except Exception as e:
        print(f"❌ PIPELINE FAILED: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_scavenger()
