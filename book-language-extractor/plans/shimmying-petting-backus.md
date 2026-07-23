# Plan: Remove Limits for Dynamic Feature Extraction

## Context
The user wants to extract *all* possible linguistic features (phrases, glossary terms, idioms, etc.) from the chapters. The current implementation is overly conservative, limiting the scope of extraction to the first 150 sentences, 5+ letter words, and a 40-term cap per chapter. Additionally, the output generator truncates these results, which prevents the user from seeing the full scope of extracted content.

## Changes
1.  **Extractor Enhancements (`extractor.py`):**
    *   **Remove Sentence Cap:** Process all sentences in a chapter.
    *   **Reduce Minimum Word Length:** Lower the word length threshold from 5 to 4 to capture more terms (e.g., "power", "trust").
    *   **Remove Term Cap:** Remove the `max_terms_per_chapter = 40` limit to allow for an exhaustive glossary of all unique, meaningful terms.
    *   **Increase Context Retention:** Allow more context sentences to be captured if needed (though 2 is a good default for many, I'll ensure it's not restricted).
    *   **Dynamic Phrase Detection (Bigrams):** Implement a basic "Bigram" (2-word phrase) detector. This will catch common phrases that aren't in a dictionary (e.g., "real-time", "data flow").

2.  **Generator Enhancements (`markdown_generator.py`):**
    *   **Remove Display Limits:** Remove the "Top 20" and "Top 12" limits. The Markdown tables will now display *all* extracted terms, idioms, and phrasal verbs.
    *   **Relax Truncation:** Increase or remove truncation limits on definitions and examples to ensure the user gets the full content they requested.

## Critical Files
- `extractor.py`
- `markdown_generator.py`

## Verification
1.  Run `python extractor.py` and compare the number of output files and the length of the glossary tables between the old and new versions.
2.  Verify that the number of terms in `outputs/chapter-01.md` is significantly higher and includes shorter words.
3.  Verify that all unique terms identified in the text are present in the output.
