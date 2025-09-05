"""Gemini API client for generating structured data."""

import google.generativeai as genai
from typing import Optional
from config.settings import settings

class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        genai.configure(api_key=settings.api_key)
        self.model = genai.GenerativeModel(settings.model_name)
    
    def test_connection(self) -> bool:
        """Test the Gemini API connection."""
        try:
            response = self.model.generate_content("Hello, Gemini! Please respond with 'Connection successful!'")
            if response and response.text:
                print("✅ Connection successful!")
                print(f"Response: {response.text}")
                return True
            else:
                print("❌ No response received")
                return False
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def generate_library_data(self, num_books: int = 5) -> Optional[str]:
        """Generate library data from Gemini API."""
        
        prompt = f"""
        Generate a JSON object representing a library with the following structure:
        - A name (string) - make it creative and interesting
        - A list of exactly {num_books} books, where each book has:
          - title (string)
          - author (string) 
          - year (integer between 1000 and 2025)
        
        Include books from different time periods and genres for variety.
        
        IMPORTANT: Return ONLY the raw JSON, no backticks, no markdown formatting, no additional text.
        
        Example format:
        {{
            "name": "The Grand Library",
            "books": [
                {{"title": "Example Title", "author": "Example Author", "year": 1999}}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
            else:
                print("❌ No response received from Gemini")
                return None
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            return None
    
    def generate_custom_prompt(self, prompt: str) -> Optional[str]:
        """Generate content from a custom prompt."""
        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
            else:
                print("❌ No response received from Gemini")
                return None
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            return None