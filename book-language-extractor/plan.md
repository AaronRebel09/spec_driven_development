# Implementation Plan: Book Language Extractor - Local Rule-Based Extraction

## Overview

The `book-language-extractor` is implemented using **local heuristic-based algorithms** with no external LLM dependencies. This approach uses regex patterns, dictionary lookups, and statistical analysis to extract linguistic features from book content.

## Architecture

### Core Components
- **Chapter Segmentation**: Identifies chapter boundaries using Markdown heading patterns (`#`, `##`, `###`)
- **Local Feature Extractor**: Implements rule-based glossary, idiom, and phrasal verb detection via regex and dictionary lookups
- **Output Generator**: Formats extracted features into structured Markdown files with tables and sections
- **Chunking Logic**: Handles long content by splitting at sentence boundaries while preserving semantic context

### Implementation Strategy
All extraction is performed locally using:
- Python standard library (`re`, `json`, `os`, `pathlib`)
- Predefined idiom/phrasal verb dictionaries (hardcoded patterns)
- Word frequency and length analysis for difficulty scoring
- Stop-word filtering for glossary term selection

## Functional Requirements (FR)

### FR 2.1.1 - Chapter Segmentation
System MUST accurately identify chapter boundaries using Markdown heading patterns:
- Regex pattern: `r'^#+\s+(.*)'` matches headings at line start
- Handles `#`, `##`, `###` heading levels
- Extracts content between chapter boundaries (start/end positions)
- Trims blank lines after headings

### FR 2.1.2 - Chapter Identification
Each extracted chapter must be associated with its correct identifier:
- Sequential IDs: `chapter-01`, `chapter-02`, etc.
- Title extraction from heading text
- Handles complex titles with subtitles and numbering

### FR 2.2.1 - Glossary Extraction
System MUST extract glossary terms using rule-based analysis:
- Regex pattern `\b[a-zA-Z]{4,}\b` identifies 4+ letter words
- Stop-word filtering excludes common English words
- Frequency analysis identifies uncommon vocabulary
- Maximum 30 unique terms per chapter to avoid duplication

### FR 2.2.2 - Idioms/Phrasal Verbs Detection
System MUST identify idiomatic expressions via dictionary lookup:
- `idiom_patterns`: Common phrasal verbs with meanings (19 entries)
- `idiom_list`: Predefined idioms and definitions (15 entries)
- Case-insensitive substring matching in chapter content
- Extracts first match per idiom pattern

### FR 2.2.3 - Definitions
System MUST provide contextual definitions:
- Automatic: "Contextual term identified in the narrative."
- Examples extracted from surrounding sentences
- Fallback to descriptive context if no match found

### FR 2.2.4 - Contextual Examples
For every extracted feature, capture at least two context sentences:
- Sentence-boundary splitting using `(?<=[.!?])\s+` pattern
- Extract first sentence containing target word
- Truncate to 80 chars if too long

### FR 2.3.1 - Output Format
Final output MUST be structured Markdown files:
- Files saved to `outputs/chapter-{ID}.md`
- Includes chapter title and reference number
- Consistent header hierarchy across all chapters

### FR 2.3.2 - Content Structure
Each output file must contain labeled sections:
- `## Glossary Words`: Table with term, POS, meaning, Spanish, example, difficulty
- `## Phrasal Verbs`: Table with phrase, meaning, notes
- `## Idioms`: Table with idiom, meaning, type (idiom/phrasal_verb)
- `## Review`: Summary section with key vocabulary highlights

### FR 2.3.3 - Translation Support
System SHOULD provide Spanish translations:
- Built-in dictionary lookup (`translations_path`)
- Fallback to `[term]` if translation unavailable
- Loaded from JSON file at startup

### FR 2.3.4 - Difficulty Scoring
Assign quantitative difficulty score based on linguistic complexity:
- Average word length analysis
- Thresholds: Low (≤4 chars), Medium (≤6 chars), High (>6 chars)
- Default to "Medium" for ambiguous cases

## Non-Functional Requirements (NFR)

### NFR 3.1.1 - Offline Operation
System MUST operate without network connectivity:
- No external API calls
- All data processed locally
- Python standard library only

### NFR 3.1.2 - Performance
Processing a book of 200,000 words must complete efficiently:
- Single-threaded regex-based processing
- No external dependencies to load/initialize
- Memory-efficient sentence-level chunking

### NFR 3.2.1 - Error Handling
System MUST handle extraction edge cases gracefully:
- Returns empty lists when no features found
- No exceptions for missing patterns
- Structured error objects for failures

### NFR 3.2.2 - Input Validation
System MUST validate input file before processing:
- File existence check
- Non-empty content verification
- Header presence validation

## Technical Design & Architecture

### Data Pipeline Flow

```
1. Ingestion (validate_input)
   ↓
2. Segmentation (detect_chapter_boundaries)
   ↓
3. Extraction (LocalExtractor.extract per chapter)
   ↓
4. Output Generation (generate_chapter_markdown)
   ↓
5. Validation (validate_output)
```

### Implementation Files

| File | Purpose |
|------|---------|
| `extractor.py` | Main pipeline: segmentation, extraction, output generation |
| `generate_chapters.py` | Utility script for tracking missing outputs |
| `tests/test_segmentation.py` | Unit tests for chapter boundary detection |
| `tests/test_pipeline.py` | End-to-end integration tests |

### Key Functions

- `detect_chapter_boundaries(content)`: Returns list of (start, end, title) tuples
- `extract_chapter_content(chapters, content)`: Splits book into structured chapter objects
- `LocalExtractor.extract(chapter_id, content)`: Performs feature extraction
- `generate_chapter_markdown(chapter_data, result)`: Formats output as Markdown
- `chunk_content(content, max_chars)`: Splits large chapters at sentence boundaries

## Verification Plan

### Unit Tests (Segmentation)
- Test basic heading detection (`#`, `##`)
- Verify blank line handling between headers
- Handle complex titles with subtitles and numbering
- Detect no-chapter case (no headers in file)

### Integration Tests (End-to-End)
- Full pipeline run with sample book
- Validate output file count matches expected chapters
- Check required sections in each output file
- Verify glossary, idioms tables populated correctly

### Error Handling Tests
- Malformed input file handling
- Empty chapter content handling
- Missing output directory creation

## Current Status: **COMPLETE**

All phases of local heuristic-based implementation are complete. The system now operates using pure rule-based extraction with no external dependencies or API calls.
