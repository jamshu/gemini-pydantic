"""Pydantic models for library and book data."""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Book(BaseModel):
    """Pydantic model for a book with validation."""
    
    title: str = Field(min_length=1, description="Book title cannot be empty")
    author: str = Field(min_length=1, description="Author name cannot be empty")
    year: int = Field(
        gt=1000,
        le=datetime.now().year,
        description="Publication year must be between 1000 and current year"
    )
    
    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        
    def __str__(self) -> str:
        """String representation of the book."""
        return f"'{self.title}' by {self.author} ({self.year})"

class Library(BaseModel):
    """Pydantic model for a library containing books."""
    
    name: str = Field(min_length=1, description="Library name cannot be empty")
    books: List[Book] = Field(description="List of books in the library")
    
    class Config:
        str_strip_whitespace = True
        validate_assignment = True
    
    def __str__(self) -> str:
        """String representation of the library."""
        return f"{self.name} ({len(self.books)} books)"
    
    def get_books_by_author(self, author: str) -> List[Book]:
        """Get all books by a specific author."""
        return [book for book in self.books if book.author.lower() == author.lower()]
    
    def get_books_after_year(self, year: int) -> List[Book]:
        """Get all books published after a specific year."""
        return [book for book in self.books if book.year > year]
    
    def get_books_before_year(self, year: int) -> List[Book]:
        """Get all books published before a specific year."""
        return [book for book in self.books if book.year < year]
    
    def get_average_publication_year(self) -> float:
        """Calculate average publication year of all books."""
        if not self.books:
            return 0.0
        return sum(book.year for book in self.books) / len(self.books)
    
    def get_unique_authors(self) -> List[str]:
        """Get list of unique authors in the library."""
        return list(set(book.author for book in self.books))
    
    def get_books_count_by_author(self) -> dict[str, int]:
        """Get count of books per author."""
        author_counts = {}
        for book in self.books:
            author_counts[book.author] = author_counts.get(book.author, 0) + 1
        return author_counts