import google.generativeai as genai
from typing import Optional, Dict, Any, List
import os
from PIL import Image

class GeminiHelper:
    def __init__(self, api_key: str):
        """
        Initialize the Gemini helper with your API key
        Args:
            api_key: Your Google API key for Gemini
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        
        try:
            # List available models
            for m in genai.list_models():
                print(f"Available model: {m.name}")
        except Exception as e:
            print(f"Error listing models: {str(e)}")
        
        # Initialize models with Gemini 2.0 Flash
        self.text_model = genai.GenerativeModel('models/gemini-2.0-flash')
        
    def generate_text(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate text using Gemini 2.0 Flash
        Args:
            prompt: The text prompt to generate from
            temperature: Controls randomness (0.0 to 1.0)
        Returns:
            Generated text response
        """
        try:
            response = self.text_model.generate_content(
                prompt,
                generation_config={"temperature": temperature}
            )
            return response.text
        except Exception as e:
            return f"Error generating text: {str(e)}"

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """
        Analyze an image using Gemini Pro Vision
        Args:
            image_path: Path to the image file
            prompt: Text prompt describing what to analyze in the image
        Returns:
            Analysis response
        """
        try:
            image = Image.open(image_path)
            response = self.text_model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f"Error analyzing image: {str(e)}"

    def chat_conversation(self, messages: List[Dict[str, str]]) -> str:
        """
        Have a chat conversation with Gemini
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
        Returns:
            Response from the model
        """
        try:
            chat = self.text_model.start_chat(history=[])
            
            for message in messages:
                if message['role'] == 'user':
                    response = chat.send_message(message['content'])
            
            return response.text
        except Exception as e:
            return f"Error in chat conversation: {str(e)}"

    def structured_analysis(self, prompt: str, output_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get structured analysis from Gemini
        Args:
            prompt: The analysis prompt
            output_structure: Dictionary defining the expected output structure
        Returns:
            Structured response matching the output_structure
        """
        try:
            # Create a prompt that requests structured output
            structured_prompt = f"""
            Please analyze the following and provide output in the exact structure specified:
            {prompt}
            
            Required output structure:
            {output_structure}
            
            Provide the response in a way that can be parsed as a Python dictionary.
            """
            
            response = self.text_model.generate_content(structured_prompt)
            # Note: You might need to add additional parsing logic here
            # depending on how Gemini formats its response
            return eval(response.text)
        except Exception as e:
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    API_KEY = os.getenv("GEMINI_API_KEY")
    
    if API_KEY:
        # Initialize the helper
        gemini = GeminiHelper(API_KEY)
        
        # Example text generation
        response = gemini.generate_text("Write a short poem about coding")
        print("Generated Text:", response)
    else:
        print("API key not found in environment variables")
    
    # Example image analysis
    # response = gemini.analyze_image("path/to/image.jpg", "What's in this image?")
    # print("Image Analysis:", response)
    
    # Example chat conversation
    chat_messages = [
        {"role": "user", "content": "What is artificial intelligence?"},
        {"role": "user", "content": "Can you give some examples?"}
    ]
    response = gemini.chat_conversation(chat_messages)
    print("Chat Response:", response)
    
    # Example structured analysis
    structure = {
        "summary": "str",
        "key_points": "list",
        "sentiment": "str"
    }
    response = gemini.structured_analysis("Analyze the impact of AI on healthcare", structure)
    print("Structured Analysis:", response) 