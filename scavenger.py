import os
import datetime
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def test_engine():
    print("Testing Gemini AI Engine...")
    
    # 1. Ask Gemini to do something
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents="Translate this to English: இது ஒரு சோதனை. Confirm you are awake in the cloud."
    )
    
    # 2. Create the reports folder 
    os.makedirs("reports", exist_ok=True)
    
    # 3. Save the output to a Markdown file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/fact_check_{timestamp}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 🛰️ System Test\n\n**Time**: {timestamp}\n\n---\n\n{response.text}")
        
    print(f"✅ Success! Report saved to {filename}")

if __name__ == "__main__":
    test_engine()
