"""File management utilities for the application."""

import os
import json
from pathlib import Path
from models.library import Library
from typing import Optional

class FileManager:
    """Manage file I/O operations for the application."""
    
    def __init__(self, output_dir: str = "output"):
        """Initialize file manager with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def save_library_json(self, library: Library, filename: str = "library_data.json") -> bool:
        """Save library data to JSON file."""
        try:
            filepath = self.output_dir / filename
            json_content = library.model_dump_json(indent=4)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_content)
            
            print(f"✅ Library data saved to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error saving JSON file: {e}")
            return False
    
    def load_library_json(self, filename: str = "library_data.json") -> Optional[Library]:
        """Load library data from JSON file."""
        try:
            filepath = self.output_dir / filename
            
            if not filepath.exists():
                print(f"❌ File not found: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                json_content = f.read()
            
            library = Library.model_validate_json(json_content)
            print(f"✅ Library data loaded from {filepath}")
            return library
        except Exception as e:
            print(f"❌ Error loading JSON file: {e}")
            return None
    
    def save_csv(self, data: dict, filename: str = "library_data.csv") -> bool:
        """Save data to CSV file."""
        try:
            import pandas as pd
            
            filepath = self.output_dir / filename
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
            
            print(f"✅ CSV data saved to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error saving CSV file: {e}")
            return False
    
    def list_output_files(self) -> list:
        """List all files in the output directory."""
        if not self.output_dir.exists():
            return []
        return [f.name for f in self.output_dir.iterdir() if f.is_file()]