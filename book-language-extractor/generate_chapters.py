"""
Utility script to identify missing chapter output files.

This function analyzes the book.md file to find all chapters and compares them
against existing files in the outputs/ directory, saving a report for tracking.
"""
import os
import re
from pathlib import Path


def find_missing_chapters():
    """
    Find which chapter output files are missing from the outputs directory.

    Reads book.md to identify all chapters (by number or title), then checks
    that corresponding chapter-{N}.md files exist in the outputs/ directory.

    Args:
        None (reads from book.md and outputs/)

    Returns:
        None, prints report of missing chapters and saves list to missing_chapters.txt
    """
    book_path = Path("book.md")
    output_dir = Path("outputs")

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    # Read the book to find chapter numbers
    with open(book_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all chapter numbers (e.g., #  4, # 5, etc.)
    chapters = re.findall(r'^#\s+(\d+)', content, re.MULTILINE)
    chapter_numbers = [int(c) for c in chapters]

    if not chapter_numbers:
        print("No chapters found in book.md.")
        return

    max_chapter = max(chapter_numbers)
    missing = []

    # Check which files are missing
    for i in range(1, max_chapter + 1):
        file_path = output_dir / f"chapter-{i:02d}.md"
        if not file_path.exists():
            missing.append(i)

    print(f"Total chapters found: {len(chapter_numbers)}")
    print(f"Missing chapters to process: {missing}")

    # Save the list to a file for tracking
    with open("missing_chapters.txt", "w") as f:
        for m in missing:
            f.write(f"Chapter {m}\n")


if __name__ == "__main__":
    find_missing_chapters()
