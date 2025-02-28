from google import genai
from dotenv import load_dotenv
import os
import json
import re
from typing import Dict, Any

# Load the .env file from ../crosschecker/
dotenv_path = os.path.join(os.path.dirname(__file__), "../crosschecker/.env")
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def ai_request(scraped_data: str, question: str) -> Dict[str, Any]:
    prompt = f"""
    The following text is extracted from a Wikipedia article:
    {scraped_data}

    Based on the information provided in the article, please find 5 articles from alternative sources (not from Wikipedia) that either confirm or refute the answer to the following question:
    Question: {question}

    Additionally, provide a brief summary of your findings regarding the question and a confidence score based on the data found. Your response should be fully in JSON format.
    Provide the URLs of the 5 articles and brief summary in the following JSON format:
    {{
        "url1": "https://example.com/article1",
        "url2": "https://example.com/article2",
        "url3": "https://example.com/article3",
        "url4": "https://example.com/article4",
        "url5": "https://example.com/article5",
        "result_summary": "Brief summary of findings.",
        "confidence_score": from 0 to 100 (int)
    }}
    """
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        result = response.text
        cleaned_result = re.sub(r'^```json|```$', '', result.strip(), flags=re.MULTILINE)
        # Parse the cleaned result into a JSON object
        result_json = json.loads(cleaned_result)
    except Exception as e:
        raise RuntimeError(f"Error while requesting API: {e}")
    return result_json
