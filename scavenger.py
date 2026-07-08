import os
import datetime
import sys

try:
    from google import genai
    from google.genai import types
except ImportError as e:
    print(f"❌ CRITICAL MAIN FRAME ERROR: Dependency binding failed: {str(e)}")
    sys.exit(1)

# Converted to the standard YouTube watch format for seamless API ingestion
TARGET_VIDEO_URL = "https://www.youtube.com/watch?v=U5FOK4sin58"

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

def run_scavenger():
    print("🛰️ Booting Cloud Scavenger System...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ENVIRONMENT ERROR: GEMINI_API_KEY is completely vacant.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    try:
        print(f"🧠 Transporting YouTube Feed ({TARGET_VIDEO_URL}) directly to Gemini 2.5 Flash Neural Net...")
        
        response = client.models.generate_content(
            # BYPASS LOCK: We use 2.5-flash which is fully unlocked on the free tier!
            model="gemini-2.5-flash",
            contents=types.Content(
                parts=[
                    types.Part(file_data=types.FileData(file_uri=TARGET_VIDEO_URL)),
                    types.Part(text=SYSTEM_PROMPT)
                ]
            ),
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],
                temperature=0.10
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

if __name__ == "__main__":
    run_scavenger()
    
