"""Data visualization functions for library data."""

import matplotlib.pyplot as plt
import pandas as pd
from models.library import Library
from analysis.data_analyzer import LibraryAnalyzer
from pathlib import Path

class LibraryVisualizer:
    """Create visualizations for library data."""
    
    def __init__(self, output_dir: str = "output"):
        """Initialize visualizer with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.analyzer = LibraryAnalyzer()
        
        # Set matplotlib style
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
    
    def plot_publication_years(self, library: Library, save: bool = True, show: bool = True) -> None:
        """Create histogram of publication years."""
        df = self.analyzer.library_to_dataframe(library)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(df['year'], bins=min(10, len(df)), edgecolor='black', alpha=0.7, color='steelblue')
        ax.set_title(f'Distribution of Publication Years - {library.name}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Publication Year', fontsize=12)
        ax.set_ylabel('Number of Books', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Add statistics text
        avg_year = df['year'].mean()
        ax.axvline(avg_year, color='red', linestyle='--', alpha=0.7, 
                  label=f'Average: {avg_year:.0f}')
        ax.legend()
        
        plt.tight_layout()
        
        if save:
            filename = self.output_dir / f"{library.name.replace(' ', '_')}_years_histogram.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Histogram saved to {filename}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def plot_books_by_decade(self, library: Library, save: bool = True, show: bool = True) -> None:
        """Create bar chart of books by decade."""
        decade_stats = self.analyzer.decade_analysis(library)
        
        if not decade_stats:
            print("❌ No decade data available for visualization")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        decades = list(decade_stats.keys())
        counts = list(decade_stats.values())
        
        bars = ax.bar(decades, counts, color='lightcoral', edgecolor='black', alpha=0.8)
        ax.set_title(f'Books by Decade - {library.name}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Decade', fontsize=12)
        ax.set_ylabel('Number of Books', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            filename = self.output_dir / f"{library.name.replace(' ', '_')}_decades_bar.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Bar chart saved to {filename}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def plot_comprehensive_analysis(self, library: Library, save: bool = True, show: bool = True) -> None:
        """Create a comprehensive multi-plot analysis."""
        df = self.analyzer.library_to_dataframe(library)
        age_stats = self.analyzer.age_analysis(library)
        decade_stats = self.analyzer.decade_analysis(library)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Comprehensive Analysis: {library.name}', fontsize=16, fontweight='bold')
        
        # 1. Publication years histogram
        ax1.hist(df['year'], bins=min(8, len(df)), edgecolor='black', alpha=0.7, color='steelblue')
        ax1.set_title('Publication Years Distribution')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Count')
        ax1.grid(True, alpha=0.3)
        
        # 2. Books by decade
        if decade_stats:
            decades = list(decade_stats.keys())
            counts = list(decade_stats.values())
            ax2.bar(decades, counts, color='lightcoral', edgecolor='black', alpha=0.8)
            ax2.set_title('Books by Decade')
            ax2.set_xlabel('Decade')
            ax2.set_ylabel('Count')
            ax2.tick_params(axis='x', rotation=45)
        
        # 3. Age categories pie chart
        age_categories = ['Classic', 'Mid-Century', 'Modern', 'Contemporary']
        age_counts = [
            age_stats['classic_books'],
            age_stats['mid_century_books'],
            age_stats['modern_books'],
            age_stats['contemporary_books']
        ]
        
        # Only include non-zero categories
        non_zero_categories = [(cat, count) for cat, count in zip(age_categories, age_counts) if count > 0]
        if non_zero_categories:
            cats, counts = zip(*non_zero_categories)
            ax3.pie(counts, labels=cats, autopct='%1.1f%%', startangle=90)
            ax3.set_title('Books by Age Category')
        
        # 4. Authors bar chart
        books_per_author = library.get_books_count_by_author()
        if len(books_per_author) <= 10:  # Only show if manageable number of authors
            authors = list(books_per_author.keys())
            counts = list(books_per_author.values())
            ax4.bar(authors, counts, color='lightgreen', edgecolor='black', alpha=0.8)
            ax4.set_title('Books per Author')
            ax4.set_xlabel('Author')
            ax4.set_ylabel('Number of Books')
            ax4.tick_params(axis='x', rotation=45)
        else:
            ax4.text(0.5, 0.5, f'{len(books_per_author)} unique authors\n(too many to display)', 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Author Distribution')
        
        plt.tight_layout()
        
        if save:
            filename = self.output_dir / f"{library.name.replace(' ', '_')}_comprehensive_analysis.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Comprehensive analysis saved to {filename}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def create_all_visualizations(self, library: Library, save: bool = True, show: bool = False) -> None:
        """Create all available visualizations for the library."""
        print(f"🎨 Creating visualizations for {library.name}...")
        
        self.plot_publication_years(library, save=save, show=show)
        self.plot_books_by_decade(library, save=save, show=show)
        self.plot_comprehensive_analysis(library, save=save, show=show)
        
        print("✅ All visualizations created successfully!")