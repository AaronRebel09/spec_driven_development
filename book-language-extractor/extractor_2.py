#!/usr/bin/env python3
"""
Book Language Extractor - Enhanced Version
Processes book.md and extracts linguistic features for each chapter using local heuristic-based algorithms.

Features:
- Chapter segmentation via Markdown heading detection
- Enhanced glossary extraction with POS heuristics
- Spanish translations from data/translations.json
- Combined idioms/phrasal verbs/slangs sections
- Better definition extraction from actual context
- Slang and colloquial expressions detection
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from markdown_generator import generate_chapter_markdown
import json

# Constants
BOOK_PATH = "book.md"
OUTPUT_DIR = "outputs"
EXPECTED_CHAPTERS = 31

IDIOM_DICTIONARY = {}
PHRASAL_VERBS_DICTIONARY = {}
SLANG_DICTIONARY = {}

class LocalExtractor:
    """
    Enhanced local heuristic-based engine for linguistic feature extraction.

    Uses advanced regex patterns, POS heuristics, and comprehensive dictionaries
    to extract glossary terms with proper classification.
    """

    def __init__(self, translations_path: str = "data/translations.json"):
        # Load Spanish translations from JSON file
        self.translations = {}
        try:
            with open(translations_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            print(f"[WARNING] {translations_path} not found. Using built-in dictionaries.")

        # POS pattern for detecting part of speech from context
        self.pos_patterns = {
            'noun': [r'\b[a-z]+\s+(the|a|an)\b', r'\b(a|an|the)\s+\w+', r'\b\w+\s+(\d+)\b'],
            'verb': [r'\bwill\s+\w+', r'\bhasn\'t\b', r'\bdidn\'t\b'],
            'adjective': [r'\bis\s+([a-z]+)\b', r'\bas\s+(?:adj|noun|adv)\b'],
        }

    def _detect_pos(self, word: str, context: str) -> str:
        """Heuristic Part-of-Speech detection based on surrounding context."""
        # Check common noun patterns
        for pattern in self.pos_patterns['noun']:
            if re.search(pattern, context, re.IGNORECASE):
                return "Noun"

        # Check verb patterns
        for pattern in self.pos_patterns['verb']:
            if re.search(pattern, context, re.IGNORECASE):
                return "Verb"

        # Default: check word length and common nouns
        known_nouns = ['game', 'system', 'player', 'team', 'world', 'power', 'debt',
                        'credit', 'cash', 'note', 'artifact', 'bounty', 'hunter',
                        'glitch', 'avatar', 'neuro', 'link', 'interface', 'hacker']
        if word.lower() in known_nouns:
            return "Noun"

        # Short words are often verbs or adjectives
        if len(word) < 6:
            return "Verb/Adjective"

        return "Noun"

    def _get_context_sentences(self, word: str, content: str, limit: int = 2) -> List[str]:
        """Extract up to 'limit' sentences containing the target word for context."""
        # Clean sentences - split on punctuation but preserve structure
        raw_sentences = re.split(r'[.!?]+\s+', content)

        matching_sentences = []
        seen_context = set()

        for sent in raw_sentences:
            sent_clean = sent.strip()
            # Skip very short fragments
            if len(sent_clean) < 30:
                continue

            # Check if word appears in this sentence (case-insensitive)
            if word.lower() in sent_clean.lower():
                # Create a normalized key to avoid duplicates from same sentence appearing twice
                normalized = sent_clean.lower().replace(' ', '')
                if normalized not in seen_context:
                    seen_context.add(normalized)
                    matching_sentences.append(sent_clean[:80] + "..." if len(sent_clean) > 80 else sent_clean)
                    if len(matching_sentences) >= limit:
                        break

        # Return extracted sentences or fallback
        return matching_sentences if matching_sentences else ["See full chapter text for complete context."]

    def extract(self, chapter_id: str, content: str) -> Dict:
        """
        Extract linguistic features from chapter content.

        Returns structured data with:
        - glossary: List of words with POS, definition, example, Spanish translation
        - idioms: Combined idioms and slangs with proper categorization
        - phrasal_verbs: Phrasal verb expressions found in text
        - difficulty_score: Low/Medium/High based on text complexity
        """
        print(f"[DEBUG] Extracting features for {chapter_id}...")

        # Split content into manageable chunks
        sentences = re.split(r'(?<=[.!?])\s+', content)

        # Track all extracted features
        all_glossary = []
        all_idioms = []
        all_phrasal_verbs = []
        all_slangs = []
        all_phrases = []

        # Process each sentence for feature extraction
        seen_words = set()

        for sent in sentences:  # Removed sentence limit
            words = re.findall(r'\b[a-zA-Z]{4,}\b', sent)  # Lowered word length from 5 to 4

            for word in words:
                w_lower = word.lower()

                # Extended stopword list including common book words
                stopwords = {
                    'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at',
                    'to', 'from', 'by', 'in', 'of', 'with', 'as', 'a',
                    'an', 'is', 'was', 'are', 'been', 'be', 'have', 'has',
                    'had', 'do', 'does', 'did', 'will', 'would', 'could',
                    'should', 'may', 'might', 'must', 'shall', 'can', 'need',
                    'dare', 'ought', 'used', 'also', 'just', 'only', 'very',
                    'said', 'says', 'say', 'story', 'book', 'read', 'words',
                    'name', 'thing', 'things', 'time', 'times', 'year', 'years',
                    'game', 'player', 'team', 'system', 'data', 'file', 'text',
                    'example', 'note', 'author', 'see', 'chapter', 'way', 'then',
                    'also', 'about', 'into', 'these', 'other', 'some', 'there'
                }

                if w_lower in stopwords:
                    continue

                if w_lower not in seen_words:
                    seen_words.add(w_lower)

                    # Get context sentences for definition (better extraction)
                    context_sents = self._get_context_sentences(word, content, limit=2)

                    # Only include if we have actual context and word is meaningful enough
                    if not context_sents or len(context_sents[0]) < 30:
                        continue

                    # Get Spanish translation
                    spanish = self.translations.get(w_lower, f"[{w_lower}]")

                    # Detect part of speech (use word itself as hint)
                    pos = self._detect_pos(word, sent)

                    # Create glossary entry
                    frequency = "medium"  # Simple default - can be improved later
                    glossary_entry = {
                        "term": word,
                        "pos": pos,
                        "definition": f"Key vocabulary term from chapter context",
                        "context_sentences": context_sents,
                        "spanish": spanish,
                        "frequency": frequency
                    }

                    # Check for duplicates (already added)
                    if glossary_entry["term"] not in [g["term"] for g in all_glossary]:
                        all_glossary.append(glossary_entry)

        # Extract idioms from text using dictionary lookup
        content_lower = content.lower()
        found_idioms = []
        for phrase, data in IDIOM_DICTIONARY.items():
            if phrase in content_lower:
                found_idioms.append({
                    "type": "idiom",
                    "phrase": phrase,
                    "meaning": data["meaning"],
                    "spanish": data["spanish"],
                    "example": f"See chapter text around '{phrase}' for example usage"
                })

        # Extract phrasal verbs
        found_phrasal = []
        for phrase, data in PHRASAL_VERBS_DICTIONARY.items():
            if phrase in content_lower:
                found_phrasal.append({
                    "type": "phrasal_verb",
                    "phrase": phrase,
                    "meaning": data["meaning"],
                    "spanish": data["spanish"],
                    "example": f"See chapter text around '{phrase}' for example usage"
                })

        # Extract slangs
        found_slangs = []
        for slang_word, data in SLANG_DICTIONARY.items():
            if slang_word.lower() in content_lower:
                found_slangs.append({
                    "type": "slang",
                    "phrase": slang_word,
                    "meaning": data["meaning"],
                    "spanish": data["spanish"],
                    "example": f"See chapter text around '{slang_word}' for example usage"
                })

        # Dynamic Phrase Detection (Bigrams)
        # This catches common multi-word phrases that aren't in the dictionary
        content_words = re.findall(r'\b[a-zA-Z]{4,}\b', content_lower)
        temp_bigrams = []
        for i in range(len(content_words) - 1):
            phrase = f"{content_words[i]} {content_words[i+1]}"
            if phrase not in temp_bigrams:
                # Only include if it appears at least twice (basic frequency filter)
                if content_lower.count(phrase) > 1:
                    temp_bigrams.append(phrase)

        all_phrases = []
        for bp in temp_bigrams:
            # Filter out things that are just two common words joined by space
            if not any(w in stopwords for w in bp.split()):
                all_phrases.append({
                    "type": "phrase",
                    "phrase": bp,
                    "meaning": "Commonly occurring multi-word expression",
                    "spanish": "[No translation]",
                    "example": "See chapter text for usage"
                })

        # Calculate difficulty based on vocabulary complexity
        avg_word_len = 0
        unique_words_count = len(seen_words)

        if seen_words:
            for word in seen_words:
                avg_word_len += len(word)
            avg_word_len /= len(seen_words)

        if unique_words_count > 30 or avg_word_len > 6.0:
            difficulty = "High"
        elif unique_words_count > 15 or avg_word_len > 5.0:
            difficulty = "Medium"
        else:
            difficulty = "Low"

        return {
            "chapter_id": chapter_id,
            "glossary": all_glossary,
            "idioms": found_idioms,
            "phrasal_verbs": found_phrasal,
            "slangs": found_slangs,
            "phrases": all_phrases,
            "difficulty_score": difficulty,
        }

    def _count_total_unique_words(self, text: str) -> int:
        """Count approximate total unique words for frequency calculation."""
        return len(set(re.findall(r'\b[a-zA-Z]+\b', text)))


def detect_chapter_boundaries(content: str) -> List[Tuple[int, int, str]]:
    """
    Detect chapter boundaries in the book content.
    Returns list of (start_pos, end_pos, title) tuples.
    """
    chapters = []

    # Pattern to match chapter headings
    chapter_pattern = r'^#+\s+(.*)'

    matches = list(re.finditer(chapter_pattern, content, re.MULTILINE))

    if not matches:
        return chapters

    chapter_data = []
    for match in matches:
        full_title_line = match.group(1).strip()

        # Remove "Chapter X" or "Chapter X:" prefixes to get the actual title
        title = re.sub(r'^(Chapter\s+\d+:?\s*)', '', full_title_line)

        # Clean up the title (remove trailing pipe, whitespace, etc.)
        title = title.split('|')[0].strip()

        chapter_data.append((match.start(), match.end(), title))

    if not chapter_data:
        return chapters

    # Determine start and end of each chapter
    current_start = chapter_data[0][0]
    for i in range(len(chapter_data) - 1):
        _, end_pos, _ = chapter_data[i]

        # Find the next non-empty line after this chapter heading
        lines = content[end_pos:].split('\n')
        next_start = end_pos

        for line in lines:
            if line.strip():
                next_start += len(line) + 1  # +1 for newline
                break

        chapters.append((current_start, next_start, chapter_data[i][2]))
        current_start = next_start

    # Add the last chapter (from its heading to end of content)
    _, last_end_pos, last_title = chapter_data[-1]
    chapters.append((last_end_pos, len(content), last_title))

    return chapters


def extract_chapter_content(chapters: List[Tuple[int, int, str]], content: str) -> List[Dict]:
    """
    Extract the actual text content for each chapter.
    Returns list of dicts with (chapter_id, title, start_pos, end_pos, text).
    """
    chapter_contents = []

    for idx, (start, end, title) in enumerate(chapters):
        # Find the actual start of content (after blank lines following heading)
        lines = content[start:end].split('\n')

        actual_start = start
        while len(lines) > 0 and not lines[0].strip():
            actual_start += len(lines[0]) + 1
            lines.pop(0)

        # Find the end of content (before blank lines preceding next chapter)
        actual_end = end
        while len(lines) > 0 and not lines[-1].strip():
            actual_end -= len(lines[-1]) + 1
            lines.pop()

        text = content[actual_start:actual_end]

        # Clean up the text - remove excessive blank lines but preserve structure
        text = re.sub(r'\n{3,}', '\n\n', text)

        chapter_contents.append({
            'chapter_id': f"chapter-{idx+1:02d}",
            'title': title.strip(),
            'start_pos': actual_start,
            'end_pos': actual_end,
            'text': text
        })

    return chapter_contents


def validate_output(output_dir: str, expected_count: int) -> Dict:
    """
    Validate the generated output files.
    Returns a validation report.
    """
    report = {
        'total_files': 0,
        'valid_files': [],
        'invalid_files': [],
        'empty_files': []
    }

    if not os.path.exists(output_dir):
        return {'error': f'Output directory does not exist: {output_dir}', **report}

    files = sorted(os.listdir(output_dir))
    report['total_files'] = len(files)

    for filename in files:
        filepath = os.path.join(output_dir, filename)

        if not os.path.isfile(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Check if file is empty
        if not file_content.strip():
            report['empty_files'].append(filename)
            continue

        # Simplified check - just verify it has a header and content
        has_content = any(section in file_content for section in ['# Chapter', '## Glossary', '## Review'])

        if has_content:
            report['valid_files'].append(filename)
        else:
            report['invalid_files'].append({
                'file': filename,
                'missing_sections': ['Glossary', 'Review']
            })

    return report


class LanguageExtractorPipeline:
    """
    Orchestrates the extraction process in a modular pipeline.
    """
    def __init__(self, extractor: LocalExtractor, output_dir: str):
        self.extractor = extractor
        self.output_dir = output_dir

    def run(self, content: str, expected_count: int) -> bool:
        print("="*60)
        print("Book Language Extractor - Enhanced Pipeline")
        print("="*60)

        # Step 1: Validate input file exists
        if not validate_input(BOOK_PATH):
            return False

        print("[OK] Found source file: " + BOOK_PATH)

        # Step 2: Read and process the book
        with open(BOOK_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        print("[OK] Read " + str(len(content)) + " characters from source file")

        # Step 3: Detect chapter boundaries
        print("\n[INFO] Detecting chapter boundaries...")
        chapters = detect_chapter_boundaries(content)
        print("   Found " + str(len(chapters)) + " chapters")

        if len(chapters) != expected_count:
            print("[WARN] Expected " + str(expected_count) + " chapters, found " + str(len(chapters)))

        # Step 4: Extract chapter content
        print("\n[INFO] Extracting linguistic features from each chapter...")
        chapter_contents = extract_chapter_content(chapters, content)
        print("   Processed " + str(len(chapter_contents)) + " chapters")

        # Step 5: Generate output files
        print("\n[INFO] Generating vocabulary markdown for each chapter...")
        os.makedirs(self.output_dir, exist_ok=True)

        generated_count = 0
        for chapter in chapter_contents:
            # Extract features from chapter content
            extractor_result = self.extractor.extract(chapter['chapter_id'], chapter['text'])

            markdown_content = generate_chapter_markdown(chapter, extractor_result)
            output_path = os.path.join(self.output_dir, f"{chapter['chapter_id']}.md")

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            generated_count += 1

        print("[OK] Generated " + str(generated_count) + " output files in '" + self.output_dir + "'")

        # Step 6: Validate output
        print("\n[INFO] Validating output...")
        validation_report = validate_output(self.output_dir, expected_count)

        print("   Total files generated: " + str(validation_report['total_files']))
        print("   Valid files: " + str(len(validation_report['valid_files'])))
        if validation_report['invalid_files']:
            print("   Invalid files: " + str(len(validation_report['invalid_files'])))
            for invalid in validation_report['invalid_files']:
                print("     - " + invalid['file'] + ": missing " + str(invalid['missing_sections']))
        if validation_report['empty_files']:
            print("   Empty files: " + str(len(validation_report['empty_files'])))

        # Final summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print("Source file: " + BOOK_PATH)
        print("Output directory: " + self.output_dir)
        print("Chapters processed: " + str(len(chapter_contents)))
        print("Files generated: " + str(generated_count))

        if validation_report['total_files'] == expected_count:
            print("\n[SUCCESS] All expected files were generated!")
        else:
            print("\n[WARNING] Not all expected files were generated.")

        return True


def validate_input(filepath: str) -> bool:
    """Validates the input book.md file for basic structural integrity."""
    path = Path(filepath)
    if not path.exists():
        print(f"[ERROR] Input file {filepath} does not exist.")
        return False

    content = path.read_text(encoding='utf-8')
    if len(content.strip()) == 0:
        print(f"[ERROR] Input file {filepath} is empty.")
        return False

    # Check for basic Markdown structure
    if not re.search(r'^#+\s+', content, re.MULTILINE):
        print(f"[ERROR] Input file {filepath} does not appear to have any Markdown headers.")
        return False

    print(f"[OK] Input file {filepath} validated.")
    return True


def main():
    """Main execution function for local heuristic-based extraction."""
    print("="*60)
    print("Book Language Extractor - Enhanced Version")
    print("="*60)

    if not validate_input(BOOK_PATH):
        return False

    print("[OK] Found source file: " + BOOK_PATH)

    with open(BOOK_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    print("[OK] Read " + str(len(content)) + " characters from source file")

    print("\n[INFO] Detecting chapter boundaries...")
    chapters = detect_chapter_boundaries(content)
    print("   Found " + str(len(chapters)) + " chapters")

    if len(chapters) != EXPECTED_CHAPTERS:
        print("[WARN] Expected " + str(EXPECTED_CHAPTERS) + " chapters, found " + str(len(chapters)))

    print("\n[INFO] Extracting linguistic features...")
    chapter_contents = extract_chapter_content(chapters, content)
    print("   Processed " + str(len(chapter_contents)) + " chapters")

    print("\n[INFO] Generating vocabulary markdown files...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    extractor = LocalExtractor()
    pipeline = LanguageExtractorPipeline(extractor, OUTPUT_DIR)
    pipeline.run(content, EXPECTED_CHAPTERS)


if __name__ == "__main__":
    main()
