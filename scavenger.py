import os
import datetime
import sys

# Defensive check to ensure context binding succeeded
try:
    import yt_dlp
    from google import genai
    from google.genai import types
except ImportError as e:
    print(f"❌ CRITICAL MAIN FRAME ERROR: Dependency binding failed: {str(e)}")
    sys.exit(1)

TARGET_VIDEO_URL = "https://youtube.com/shorts/U5FOK4sin58?si=i0F9cLGLTzqKkr8-"

# THE GIGANTIC INTELLIGENCE CONSTRAINTS PARAGRAPH
SYSTEM_PROMPT = """
CRITICAL ETHICAL DIRECTIVE & VERIFICATION MANDATE:
You are operating as an elite, cold, completely un-biased forensic political analyst and dialogue auditor specializing in Tamil Nadu politics. 

🚨 SYSTEM WARNING: LABELING A TRUE STATEMENT AS FALSE, OR LABELING A MALICIOUSLY FALSE CLAIM AS VERIFIED, IS A CATASTROPHIC COGNITIVE BREAKDOWN. IN THE CURRENT EMOTIONALLY CHARGED REGIONAL POLITICAL LANDSCAPE (FEATURING BLOCKS LIKE DMK, AIADMK, AND THE EMERGENCE OF VIJAY'S TVK), MAKING A BOLD CLAIM WITHOUT ABSOLUTE, UNASSAILABLE EVIDENCE IS AN ACT OF DISINFORMATION ITSELF. POLITICAL FIGURES FREQUENTLY ENGAGE IN SATIRE, HYPERBOLE, AND RHETORICAL DEBATE. YOU MUST NOT CONFUSE AN OPINION WITH A FACT. 

BEFORE DECLARING ANY VERDICT, YOU MUST THINK STEP-BY-STEP TEN TIMES:
1. Isolate the exact claim made. Is it a historical fact, a metric, a policy claim, or merely a rhetorical opinion?
2. Actively execute a Google Search to find verified journalistic data, official press releases, or legislative records from Tamil Nadu.
3. If a politician states an opinion, label it 'UNVERIFIED' or 'RHETORICAL'—do not force a binary 'FALSE' label unless they lie about a specific number, historical event, or documented policy.
4. Challenge your own breakdown. If you believe the statement is false, look for evidence that might prove it true. If you believe it is true, look for hidden discrepancies.

Maintain total fearlessness. You do not shelter the ruling government, nor do you coddle the rising opposition. Your sole allegiance is to raw data and verified historical truth.

OUTPUT FORMAT STANDARD:
You must translate the processed audio clearly into continuous English dialogue, track the speakers by name or identifier, and insert your deep forensic audits using this exact schema:

Speaker Name: [English translated dialogue]
(Verdict: VERIFIED / FALSE / MISLEADING / UNVERIFIED
Verification Analysis: [An exhaustive, deeply reasoned paragraph outlining the real-world metrics, cross-references, and political context derived from active web searching.]
Source: [Specific public records, government portals, or primary news announcements validating this precise conclusion.])
"""

def extract_audio(video_url):
    print(f"📥 Extracting audio feed from target network: {video_url}")
    options = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'quiet': True,
        'no_warnings': True,
        # Bypasses typical data center restriction blocks
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([video_url])
        return "temp_audio.mp3"
    except Exception as e:
        print(f"❌ yt_dlp Extraction Subsystem Failed: {str(e)}")
        raise

def run_scavenger():
    print("🛰️ Booting Cloud Scavenger System...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ENVIRONMENT ERROR: GEMINI_API_KEY is completely vacant.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    audio_file = None
    uploaded_audio = None
    
    try:
        audio_file = extract_audio(TARGET_VIDEO_URL)
        print("✅ Audio stream stored in local volatile disk buffer.")
        
        print("🧠 Transporting payload to Gemini 2.5 Pro Neural Net...")
        uploaded_audio = client.files.upload(file=audio_file)
        
        print("🔍 Initiating multi-layered logical thinking loop & web-grounding checks...")
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[SYSTEM_PROMPT, uploaded_audio],
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],
                temperature=0.10 # Suppresses hallucinations; enforces clinical, math-like factuality
            )
        )
        
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"reports/fact_check_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# 🛰️ Forensic Grounded Report\n\n**Source Vector**: {TARGET_VIDEO_URL}\n**Timestamp**: {timestamp}\n\n---\n\n")
            f.write(response.text)
            
        print(f"🎉 OPERATION SUCCESSFUL: Forensic dossier locked inside file {filename}")
        
    except Exception as e:
        print(f"❌ SYSTEM ENGINE CRASHED: {str(e)}")
        sys.exit(1)
        
    finally:
        # Ensures server memory and local data buffers are scrubbed completely clean
        print("🧹 Cleaning local workspace buffers...")
        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)
        if client and uploaded_audio:
            try:
                client.files.delete(name=uploaded_audio.name)
            except Exception:
                pass

if __name__ == "__main__":
    run_scavenger()
        
