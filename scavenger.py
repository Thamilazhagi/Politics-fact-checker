import os
import datetime
import sys

try:
    from google import genai
except ImportError:
    print("❌ ERROR: The 'google-genai' library is not installed properly.")
    sys.exit(1)

def test_engine():
    print("🛰️ Starting Cloud Engine Diagnostic...")
    
    # Force the script to read the key explicitly
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: 'GEMINI_API_KEY' is missing!")
        sys.exit(1)
        
    print("✅ API Key found. Initializing Gemini Client...")
    
    try:
        # Force-feed the key to the client to avoid SDK guessing games
        client = genai.Client(api_key=api_key)
        
        # Using FLASH: The most reliable and universally available free model
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Translate this to English: இது ஒரு சோதனை. Confirm you are awake in the cloud."
        )
        
        # Create reports directory
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"reports/fact_check_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# 🛰️ System Test\n\n**Time**: {timestamp}\n\n---\n\n{response.text}")
            
        print(f"🎉 SUCCESS! Report generated and saved locally to {filename}")
        
    except Exception as e:
        print(f"❌ API CALL FAILED: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_engine()
    
