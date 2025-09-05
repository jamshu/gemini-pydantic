"""Basic example of using the Gemini-Pydantic integration."""

from services.data_processor import DataProcessor
from utils.file_manager import FileManager
from analysis.data_analyzer import LibraryAnalyzer

def main():
    """Run basic example workflow."""
    print("🚀 Basic Gemini-Pydantic Example")
    print("=" * 40)
    
    # Initialize components
    processor = DataProcessor()
    file_manager = FileManager()
    analyzer = LibraryAnalyzer()
    
    # Test connection first
    print("Testing Gemini connection...")
    if not processor.gemini_client.test_connection():
        print("❌ Failed to connect to Gemini. Please check your API key.")
        return
    
    # Generate and parse library data
    print("\n📚 Generating library data...")
    library = processor.generate_and_parse_library(num_books=5)
    
    if not library:
        print("❌ Failed to generate library data")
        return
    
    # Display basic information
    print(f"\n✅ Successfully created library: {library.name}")
    print(f"Number of books: {len(library.books)}")
    print("\nBooks in the library:")
    for i, book in enumerate(library.books, 1):
        print(f"  {i}. {book}")
    
    # Save to file
    print("\n💾 Saving to file...")
    file_manager.save_library_json(library, "basic_example_library.json")
    
    # Basic analysis
    print("\n📊 Basic Analysis:")
    stats = analyzer.basic_statistics(library)
    print(f"  • Unique authors: {stats['unique_authors']}")
    print(f"  • Year range: {stats['year_range']['earliest']} - {stats['year_range']['latest']}")
    print(f"  • Average publication year: {stats['average_publication_year']}")
    
    print("\n✅ Basic example completed successfully!")

if __name__ == "__main__":
    main()