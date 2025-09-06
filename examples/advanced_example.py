"""Advanced example of using the Gemini-Pydantic integration."""

from services.data_processor import DataProcessor
from utils.file_manager import FileManager
from analysis.data_analyzer import LibraryAnalyzer

def main():
    """Run advanced example workflow."""
    print("🚀 Advanced Gemini-Pydantic Example")
    print("=" * 50)
    
    # Initialize components
    processor = DataProcessor()
    file_manager = FileManager()
    analyzer = LibraryAnalyzer()
    
    # Test connection
    print("Testing Gemini connection...")
    if not processor.gemini_client.test_connection():
        print("❌ Failed to connect to Gemini. Please check your API key.")
        return
    
    # Generate multiple libraries
    print("\n📚 Generating libraries...")
    libraries = []

    library = processor.generate_and_parse_library(num_books=20)
    if library:
        libraries.append(library)
        print(f"  ✅ Created library with {len(library.books)} books")
    else:
        print(f"  ❌ Failed to generate library")

    library = processor.generate_and_parse_library(num_books=15)
    if library: 
        libraries.append(library)
        print(f"  ✅ Created library with {len(library.books)} books")
    
    # Save all libraries to JSON
    print("\n💾 Saving libraries to files...")
    for lib in libraries:
        filename = f"advanced_{lib.name.lower().replace(' ', '_')}.json"
        file_manager.save_library_json(lib, filename)
        print(f"  • Saved {lib.name} → {filename}")
    
    # Run advanced analysis
    print("\n📊 Running advanced analysis...")
    overall_stats = analyzer.overall_statistics(libraries)
    library_stats = analyzer.library_statistics(libraries)
    
    print("\n📈 Overall Statistics:")
    print(f"  • Total books: {overall_stats['total_books']}")
    print(f"  • Average pages: {overall_stats['avg_pages']}")
    print(f"  • Average rating: {overall_stats['avg_rating']}")
    print(f"  • Genre distribution: {overall_stats['genre_distribution']}")
    
    print("\n🏛 Per-Library Statistics:")
    for lib, stats in library_stats.items():
        print(f"  {lib}: {stats}")
    
    # Export advanced results
    print("\n💾 Exporting results...")
    file_manager.save_libraries_excel(libraries, "advanced_library_analysis.xlsx")
    analyzer.create_visualizations(libraries, "advanced_library_analysis.png")
    analyzer.create_genre_deep_dive(libraries, "advanced_genre_deep_dive.png")
    
    print("\n🎉 Advanced example completed successfully!")
    print("Results saved to: advanced_library_analysis.xlsx, advanced_library_analysis.png, advanced_genre_deep_dive.png")

if __name__ == "__main__":
    main()
