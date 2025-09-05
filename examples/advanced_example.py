import random
import string
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict

# ----------------------
# Book & Library Classes
# ----------------------
class Book:
    def __init__(self, title: str, author: str, genre: str, pages: int, rating: float):
        self.title = title
        self.author = author
        self.genre = genre
        self.pages = pages
        self.rating = rating

    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'pages': self.pages,
            'rating': self.rating
        }

class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: List[Book] = []

    def add_book(self, book: Book):
        self.books.append(book)

    def generate_random_books(self, num_books: int):
        genres = ['Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 'Non-Fiction']
        for _ in range(num_books):
            title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            author = ''.join(random.choices(string.ascii_uppercase, k=3))
            genre = random.choice(genres)
            pages = random.randint(100, 1000)
            rating = round(random.uniform(1.0, 5.0), 2)
            self.add_book(Book(title, author, genre, pages, rating))

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([book.to_dict() for book in self.books])

# ----------------------
# Analysis Class
# ----------------------
class BookAnalysis:
    def __init__(self, libraries: List[Library]):
        self.libraries = libraries

    def overall_statistics(self):
        all_books = [book for lib in self.libraries for book in lib.books]
        total_books = len(all_books)
        avg_pages = statistics.mean([b.pages for b in all_books])
        avg_rating = statistics.mean([b.rating for b in all_books])
        genres = {}
        for b in all_books:
            genres[b.genre] = genres.get(b.genre, 0) + 1
        return {
            'total_books': total_books,
            'avg_pages': round(avg_pages, 2),
            'avg_rating': round(avg_rating, 2),
            'genre_distribution': genres
        }

    def library_statistics(self):
        stats = {}
        for lib in self.libraries:
            ratings = [b.rating for b in lib.books]
            stats[lib.name] = {
                'num_books': len(lib.books),
                'avg_rating': round(statistics.mean(ratings), 2) if ratings else 0,
                'median_rating': round(statistics.median(ratings), 2) if ratings else 0
            }
        return stats

# ----------------------
# Export Helpers
# ----------------------
def export_to_excel(libraries: List[Library], filename: str):
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        all_books = [book.to_dict() for lib in libraries for book in lib.books]
        pd.DataFrame(all_books).to_excel(writer, sheet_name='All_Books', index=False)

        for lib in libraries:
            lib.to_dataframe().to_excel(writer, sheet_name=lib.name, index=False)

        genre_stats = {}
        for lib in libraries:
            for book in lib.books:
                genre_stats[book.genre] = genre_stats.get(book.genre, 0) + 1
        pd.DataFrame(list(genre_stats.items()), columns=['Genre', 'Count']).to_excel(
            writer, sheet_name='Genre_Stats', index=False
        )

def create_visualizations(libraries: List[Library]):
    all_books = [book for lib in libraries for book in lib.books]
    df = pd.DataFrame([b.to_dict() for b in all_books])

    plt.figure(figsize=(14, 6))

    # Rating Distribution
    plt.subplot(1, 2, 1)
    sns.histplot(df['rating'], bins=20, kde=True)
    plt.title('Rating Distribution')

    # Genre Distribution
    plt.subplot(1, 2, 2)
    sns.countplot(x='genre', data=df)
    plt.title('Genre Distribution')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('library_analysis.png')
    plt.close()

def create_genre_deep_dive(libraries: List[Library]):
    all_books = [book for lib in libraries for book in lib.books]
    df = pd.DataFrame([b.to_dict() for b in all_books])

    plt.figure(figsize=(12, 6))

    # Boxplot
    plt.subplot(1, 2, 1)
    sns.boxplot(x='genre', y='rating', data=df)
    plt.title('Ratings by Genre')
    plt.xticks(rotation=45)

    # Scatter Plot (pages vs rating)
    plt.subplot(1, 2, 2)
    genres = df['genre'].unique()
    palette = sns.color_palette("husl", len(genres))
    genre_colors = {genre: palette[i] for i, genre in enumerate(genres)}
    for genre in genres:
        subset = df[df['genre'] == genre]
        plt.scatter(subset['pages'], subset['rating'], color=genre_colors[genre], alpha=0.6, label=genre)
    plt.xlabel('Pages')
    plt.ylabel('Rating')
    plt.title('Pages vs Rating (by Genre)')
    plt.legend()

    plt.tight_layout()
    plt.savefig('genre_deep_dive.png')
    plt.close()

# ----------------------
# Main
# ----------------------
def main():
    # Create libraries with random books
    libraries = [Library("Central"), Library("Community"), Library("University")]
    for lib in libraries:
        lib.generate_random_books(50)

    # Run analysis
    analysis = BookAnalysis(libraries)
    overall_stats = analysis.overall_statistics()
    library_stats = analysis.library_statistics()

    # Export results
    export_to_excel(libraries, "library_analysis.xlsx")
    create_visualizations(libraries)
    create_genre_deep_dive(libraries)

    # Print summaries
    print("\n📊 OVERALL STATISTICS")
    print(overall_stats)
    print("\n🏛 LIBRARY STATISTICS")
    for lib, stats in library_stats.items():
        print(f"{lib}: {stats}")

    print("\n🎉 Analysis completed! Results saved to 'library_analysis.xlsx', 'library_analysis.png', and 'genre_deep_dive.png'")

if __name__ == "__main__":
    main()
