"""Data analysis functions for library data."""

import pandas as pd
from models.library import Library
from datetime import datetime
from typing import Dict, Any

class LibraryAnalyzer:
    """Analyze library data and generate insights."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.current_year = datetime.now().year
    
    def library_to_dataframe(self, library: Library) -> pd.DataFrame:
        """Convert library data to a Pandas DataFrame."""
        data = {
            'title': [book.title for book in library.books],
            'author': [book.author for book in library.books],
            'year': [book.year for book in library.books]
        }
        return pd.DataFrame(data)
    
    def basic_statistics(self, library: Library) -> Dict[str, Any]:
        """Generate basic statistics about the library."""
        df = self.library_to_dataframe(library)
        
        stats = {
            'library_name': library.name,
            'total_books': len(library.books),
            'unique_authors': df['author'].nunique(),
            'year_range': {
                'earliest': df['year'].min(),
                'latest': df['year'].max()
            },
            'average_publication_year': round(df['year'].mean(), 1),
            'median_publication_year': df['year'].median(),
            'books_per_author': library.get_books_count_by_author()
        }
        
        return stats
    
    def decade_analysis(self, library: Library) -> Dict[str, int]:
        """Analyze books by decade."""
        df = self.library_to_dataframe(library)
        df['decade'] = (df['year'] // 10) * 10
        decade_counts = df['decade'].value_counts().sort_index()
        
        return {f"{decade}s": count for decade, count in decade_counts.items()}
    
    def age_analysis(self, library: Library) -> Dict[str, Any]:
        """Analyze books by age categories."""
        df = self.library_to_dataframe(library)
        df['age'] = self.current_year - df['year']
        
        # Define age categories
        classic = df[df['year'] < 1950]
        mid_century = df[(df['year'] >= 1950) & (df['year'] < 1980)]
        modern = df[(df['year'] >= 1980) & (df['year'] < 2000)]
        contemporary = df[df['year'] >= 2000]
        
        return {
            'classic_books': len(classic),
            'mid_century_books': len(mid_century),
            'modern_books': len(modern),
            'contemporary_books': len(contemporary),
            'average_age': round(df['age'].mean(), 1),
            'oldest_book': {
                'title': df.loc[df['year'].idxmin(), 'title'],
                'year': df['year'].min(),
                'age': self.current_year - df['year'].min()
            },
            'newest_book': {
                'title': df.loc[df['year'].idxmax(), 'title'],
                'year': df['year'].max(),
                'age': self.current_year - df['year'].max()
            }
        }
    
    def generate_report(self, library: Library) -> str:
        """Generate a comprehensive analysis report."""
        basic_stats = self.basic_statistics(library)
        decade_stats = self.decade_analysis(library)
        age_stats = self.age_analysis(library)
        
        report = f"""
📚 LIBRARY ANALYSIS REPORT
{'=' * 50}

Library: {basic_stats['library_name']}
Total Books: {basic_stats['total_books']}
Unique Authors: {basic_stats['unique_authors']}

📅 TEMPORAL ANALYSIS
Publication Range: {basic_stats['year_range']['earliest']} - {basic_stats['year_range']['latest']}
Average Publication Year: {basic_stats['average_publication_year']}
Median Publication Year: {basic_stats['median_publication_year']}

📊 BOOKS BY DECADE:
"""
        for decade, count in decade_stats.items():
            report += f"  {decade}: {count} book(s)\n"
        
        report += f"""
🏛️ AGE CATEGORIES:
  Classic (pre-1950): {age_stats['classic_books']} books
  Mid-Century (1950-1979): {age_stats['mid_century_books']} books
  Modern (1980-1999): {age_stats['modern_books']} books
  Contemporary (2000+): {age_stats['contemporary_books']} books

📖 NOTABLE BOOKS:
  Oldest: "{age_stats['oldest_book']['title']}" ({age_stats['oldest_book']['year']}) - {age_stats['oldest_book']['age']} years old
  Newest: "{age_stats['newest_book']['title']}" ({age_stats['newest_book']['year']}) - {age_stats['newest_book']['age']} years old

👥 AUTHORS:
"""
        
        for author, count in basic_stats['books_per_author'].items():
            report += f"  {author}: {count} book(s)\n"
        
        return report