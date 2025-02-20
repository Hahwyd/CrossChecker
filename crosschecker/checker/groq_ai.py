from groq import Groq
from dotenv import load_dotenv
import os

# Load the .env file from ../crosschecker/
dotenv_path = os.path.join(os.path.dirname(__file__), "../crosschecker/.env")
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("GROQ_API_KEY")

# if not api_key: # Need to add to logging
#     raise ValueError("GROQ_API_KEY is not set in the environment variables")

client = Groq(api_key=api_key)


def groq_request(scraped_data, question): #Need to add to logging
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
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        result = chat_completion.choices[0].message.content
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

text1 = """
 The tomato (US: /təmeɪtoʊ/, UK: /təmɑːtoʊ/), Solanum lycopersicum, is a plant whose fruit is an edible berry that is eaten as a vegetable. The tomato is a member of the nightshade family that includes tobacco, potato, and chili peppers. It originated from and was domesticated in western South America. It was introduced to the Old World by the Spanish in the Columbian exchange in the 16th century.
 Tomato plants are vines, largely annual and vulnerable to frost, though sometimes living longer in greenhouses. The flowers are able to self-fertilise. Modern varieties have been bred to ripen uniformly red, in  a process that has impaired the fruit's sweetness and flavor. There are thousands of cultivars, varying in size, color, shape, and flavor. Tomatoes are attacked by many insect pests and nematodes, and are subject to diseases caused by viruses and by mildew and blight fungi.
 """
print(groq_request(text1, "Is this true?"))