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

    Based on the information provided in the article, please analyze the following question:
    Question: {question}

    Provide a brief summary answering the question based on the article's content. Then, find 5 articles from alternative sources (not Wikipedia) that either confirm or refute your answer. Ensure that all provided URLs are currently active and accessible (i.e., not outdated or broken links). Verify the functionality of each link before including it in your response. If a link is inaccessible, replace it with a working alternative.

    Evaluate the reliability of your answer based on the Wikipedia article and the alternative sources.

    Return your response in JSON format with:
    - A summary of your findings directly answering the question.
    - A confidence score (0 to 100) reflecting how certain you are in the accuracy and reliability of your provided summary, based on the consistency and quality of the information from the Wikipedia article and the alternative sources. For example, if your answer is well-supported by consistent data, the score should be close to 100; if the data is contradictory or insufficient, the score should be lower.
    - URLs of the 5 articles, all confirmed to be working.

    Format your response as:
    {{
        "url1": "https://example.com/article1",
        "url2": "https://example.com/article2",
        "url3": "https://example.com/article3",
        "url4": "https://example.com/article4",
        "url5": "https://example.com/article5",
        "result_summary": "Brief summary answering the question based on the article and sources.",
        "confidence_score": integer from 0 to 100
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
