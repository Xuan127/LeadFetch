from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def product_description_to_query(product_description):
    prompt = f"""
            You are a world-class marketer. Given the following product description, 
            generate a single search query that we can look for influencers on social media.
            We want to look for influencers that is using products from the same market but not using our products yet.
            So you should output a query that will lead to a potential market that we can expand in.
            Dont include and hashtags, logical operators or special characters.
            Just output a short search query in text, it should be simple keywords.
            Product description: {product_description}"""
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0
        ),
    )

    return response
    

if __name__ == "__main__":
    product_description = "ElevenLabs is an AI audio research and deployment company. Our mission is to make content universally accessible in any language and in any voice. Our research team develops AI audio models that generate realistic, versatile and contextually-aware speech, voices, and sound effects across 32 languages."
    response = product_description_to_query(product_description)
    print(response.text)
