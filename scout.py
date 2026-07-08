import os
import datetime
import json
import feedparser
from groq import Groq
from google import genai
from google.genai import types

# The actual RSS feeds of major TN news networks
TARGET_CHANNELS = [
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCmyKnNRH0wH-r8I-ceP-dsg", # Puthiya Thalaimurai
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC-JFyL0zDFOsPMpuWu39rPA", # Thanthi TV
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC8Z-VjXBtDJTvq6aqkIskPg"  # Polimer News
]

# 2026 Political Radar Matrix
KEYWORDS = [
    "Vijay", "Stalin", "Edappadi", "EPS", "Annamalai", "Seeman", 
    "Thirumavalavan", "Mahendran", "Udhayanidhi", "Ramadoss",
    "TVK", "DMK", "AIADMK", "BJP", "NTK", "VCK", "Congress", "PMK",
    "CM", "Chief Minister", "Power Cut", "Current", "Minsaram", 
    "Assembly", "Press Meet", "Interview", "Speech", "Live", 
    "Protest", "Arrest", "Scandal", "Election"
]

MAX_GEMINI_CALLS_PER_DAY = 45

# Llama 3.1 Prompt (Title reading only)
SCOUT_PROMPT = """
You are a rapid-filter AI. Is this YouTube video title about Tamil Nadu politics, a political speech, a press meet, or a government administrative issue?
Answer ONLY with the word "YES" or "NO". Do not say anything else.
"""

# Gemini 2.5 Prompt (Full video analysis)
HEAVY_PROMPT = """
CRITICAL ETHICAL DIRECTIVE: You are an elite, cold, un-biased forensic political analyst. 

OUTPUT FORMAT:
1. Identify the speakers by their ACTUAL NAMES. 
2. Translate the dialogue clearly into continuous English.
3. Fact-check using this exact schema:

[Actual Speaker Name]: [English translated dialogue]
(Verdict: VERIFIED / FALSE / MISLEADING / UNVERIFIED
Verification Analysis: [Deeply reasoned paragraph outlining real-world metrics, cross-references, and 2026 political context derived from active web searching.]
Source: [Specific public records or official announcements])
"""

def load_db():
    if not os.path.exists("database.json"):
        return {"date": str(datetime.date.today()), "api_calls_today": 0, "backlog": []}
    with open("database.json", "r") as f:
        return json.load(f)

def save_db(db):
    with open("database.json", "w") as f:
        json.dump(db, f, indent=4)

def run_scout():
    print("🛰️ Waking up the Hybrid-Cloud Intelligence Scout...")
    db = load_db()
    today_str = str(datetime.date.today())
    
    if db.get("date") != today_str:
        db["date"] = today_str
        db["api_calls_today"] = 0
        
    heavy_key = os.environ.get("GEMINI_API_KEY")
    scout_key = os.environ.get("GROQ_API_KEY")
    
    if not heavy_key or not scout_key:
        print("❌ CRITICAL ERROR: Missing GEMINI_API_KEY or GROQ_API_KEY.")
        return
        
    heavy_client = genai.Client(api_key=heavy_key)
    scout_client = Groq(api_key=scout_key)

    new_videos = []
    
    # PHASE 1: Llama scans the RSS feeds (Free & Instant)
    print("📡 Groq Radar scanning RSS feeds...")
    for feed_url in TARGET_CHANNELS:
        feed = feedparser.parse(feed_url)
        # Scan the 10 newest videos from each channel
        for entry in feed.entries[:10]:
            title = entry.title
            link = entry.link
            
            # Pre-filter: Only ping Groq if a keyword is in the title
            if any(k.lower() in title.lower() for k in KEYWORDS) and link not in str(db["backlog"]):
                try:
                    scout_response = scout_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": SCOUT_PROMPT},
                            {"role": "user", "content": f"Title: {title}"}
                        ],
                        temperature=0.1
                    )
                    
                    answer = scout_response.choices[0].message.content.strip().upper()
                    if "YES" in answer:
                        print(f"🎯 Groq identified target: {title}")
                        new_videos.append({"title": title, "url": link})
                    else:
                        print(f"⏭️ Groq ignored: {title}")
                except Exception as e:
                    print(f"⚠️ Groq API Failed on title: {e}")

    # PHASE 2: Gemini watches the target videos
    for video in new_videos:
        if db["api_calls_today"] < MAX_GEMINI_CALLS_PER_DAY:
            print(f"🧠 Gemini Heavy Brain analyzing video: {video['title']}")
            try:
                response = heavy_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=types.Content(
                        parts=[
                            types.Part(file_data=types.FileData(file_uri=video['url'])),
                            types.Part(text=HEAVY_PROMPT)
                        ]
                    ),
                    config=types.GenerateContentConfig(tools=[{"google_search": {}}], temperature=0.10)
                )
                
                os.makedirs("reports", exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                safe_title = "".join([c for c in video['title'] if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                filename = f"reports/{timestamp}_{safe_title[:30].replace(' ', '_')}.md"
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"# 🛰️ Grounded Report: {video['title']}\n**Source**: {video['url']}\n\n---\n\n{response.text}")
                
                db["api_calls_today"] += 1
                print(f"✅ Report generated. Gemini API used today: {db['api_calls_today']}/{MAX_GEMINI_CALLS_PER_DAY}")
                
            except Exception as e:
                print(f"❌ Gemini Failed on {video['url']}: {e}")
        else:
            print(f"⚠️ GEMINI QUOTA REACHED. Pushing to backlog: {video['title']}")
            if video not in db["backlog"]:
                db["backlog"].append(video)
                
    save_db(db)

if __name__ == "__main__":
    run_scout()
      
