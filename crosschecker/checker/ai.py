from google import genai
from dotenv import load_dotenv
import os

# Load the .env file from ../crosschecker/
dotenv_path = os.path.join(os.path.dirname(__file__), "../crosschecker/.env")
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("GEMINI_API_KEY")

# if not api_key: # Need to add to logging
#     raise ValueError("GROQ_API_KEY is not set in the environment variables")

client = genai.Client(api_key=api_key)


def ai_request(scraped_data, question):  # Need to add to logging
    try:
        prompt = f"""
        The following text is extracted from a Wikipedia article:
        {scraped_data}

        Based on the information provided in the article, please find 5 articles from alternative sources (not from Wikipedia) that either confirm or refute the answer to the following question:
        Question: {question}

        Provide the URLs of the 5 articles in the following JSON format:
        {{
            "url1": "https://example.com/article1",
            "url2": "https://example.com/article2",
            "url3": "https://example.com/article3",
            "url4": "https://example.com/article4",
            "url5": "https://example.com/article5"
        }}

        Additionally, provide a brief summary of your findings regarding the question.
        """
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
