import os
import sys
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_tests_from_feature(feature_path: str, language: str = "python"):
    """Use Groq to generate test scenarios - free tier available."""
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    with open(feature_path, "r") as f:
        feature_content = f.read()
    
    prompt = f"""
You are a QA engineer. Given this feature description, generate comprehensive test cases.

Feature:
{feature_content}

Generate test cases in {language}. Requirements:
- Cover happy path, edge cases, and error cases
- Use pytest (Python) or Jest (TypeScript)
- Include clear test names describing what is being tested
- Add comments explaining the intent of each test group
- Return ONLY the code, no explanation

For Python, use pytest with a mock/stub pattern (no real HTTP calls).
For TypeScript, use Jest with mock functions.
"""

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        messages=[{"role": "user", "content": prompt}],
        # gpt-oss reasons before answering and those tokens count towards the limit
        max_tokens=8000
    )
    
    return response.choices[0].message.content