"""Data processing utilities for library data."""

from models.library import Library, Book
from utils.json_cleaner import JSONCleaner
from services.gemini_client import GeminiClient
from typing import Optional
import json

class DataProcessor:
    """Process and validate library data from Gemini responses."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.gemini_client = GeminiClient()
        self.json_cleaner = JSONCleaner()
    
    def generate_and_parse_library(self, num_books: int = 5) -> Optional[Library]:
        """Complete workflow: Generate -> Clean -> Validate -> Return Library."""
        
        print(f"🔄 Generating library data with {num_books} books...")
        
        # Step 1: Generate raw data from Gemini
        raw_response = self.gemini_client.generate_library_data(num_books)
        if not raw_response:
            print("❌ Failed to generate data from Gemini")
            return None
        
        # Step 2: Clean and validate JSON
        try:
            cleaned_json = self.json_cleaner.clean_json_response(raw_response)
            print("✅ JSON cleaned successfully")
            
            # Step 3: Parse and validate with Pydantic
            library = Library.model_validate_json(cleaned_json)
            print("✅ Data validated and parsed successfully!")
            
            return library
            
        except Exception as e:
            print(f"❌ Error processing data: {e}")
            print(f"Raw response: {raw_response}")
            return None
    
    def parse_json_to_library(self, json_string: str) -> Optional[Library]:
        """Parse a JSON string directly to Library object."""
        try:
            cleaned_json = self.json_cleaner.clean_json_response(json_string)
            library = Library.model_validate_json(cleaned_json)
            print("✅ Successfully parsed JSON to Library object")
            return library
        except Exception as e:
            print(f"❌ Error parsing JSON: {e}")
            return None
    
    def library_to_dict(self, library: Library) -> dict:
        """Convert Library object to dictionary."""
        return library.model_dump()
    
    def library_to_json(self, library: Library, indent: int = 4) -> str:
        """Convert Library object to formatted JSON string."""
        return library.model_dump_json(indent=indent)