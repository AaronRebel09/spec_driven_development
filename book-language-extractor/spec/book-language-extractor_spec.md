# Specification: Book Language Extractor

**Version:** 1.0.0 (Initial Draft)
**Date:** 2026-06-21
**Status:** Ready for Use - Local Rule-Based Extraction

## 1. Introduction and Goals

This document specifies the requirements, design, and constraints for the `book-language-extractor` feature. The primary goal is to process a source `book.md` file, segment its content into chapters, and extract specific linguistic features (glossary terms, idioms, definitions) for each chapter using **local heuristic-based algorithms** to produce structured Markdown output.

## 2. Functional Requirements (The "What")

### 2.1 Chapter Segmentation
*   **FR 2.1.1:** The system **MUST** accurately identify and segment the `book.md` into discrete chapters based on predefined structural markers (e.g., Markdown headings like `# Chapter X`).
*   **FR 2.1.2:** Each extracted chapter must be associated with its correct sequential chapter identifier.

### 2.2 Linguistic Feature Extraction
For every identified chapter, the system **MUST** perform the following extractions:
*   **FR 2.2.1 (Glossary):** Extract a list of key glossary terms found in the chapter text using regex-based pattern matching and word frequency analysis.
*   **FR 2.2.2 (Idioms/Phrasal Verbs):** Identify and extract idiomatic expressions and phrasal verbs using predefined dictionary lookup.
*   **FR 2.2.3 (Definitions):** Generate contextual definitions for extracted terms based on surrounding text analysis.
*   **FR 2.2.4 (Contextual Examples):** For every extracted feature, the system **MUST** capture at least two surrounding sentences to provide context for the term/idiom.

### 2.3 Data Structuring and Output
*   **FR 2.3.1 (Output Format):** The final output for each chapter **MUST** be a structured Markdown file (`outputs/chapter_{ID}.md`).
*   **FR 2.3.2 (Content Structure):** Each output file must contain distinct, clearly labeled sections for: Glossary, Idioms, and Contextual Examples.
*   **FR 2.3.3 (Translation):** The system **SHOULD** attempt to provide Spanish translations where available from a built-in dictionary resource.
*   **FR 2.3.4 (Difficulty Scoring):** A difficulty score (e.g., Low, Medium, High) **MUST** be assigned to the chapter content based on word length and vocabulary complexity analysis.

## 3. Non-Functional Requirements (The "How Well")

### 3.1 Performance
*   **NFR 3.1.1 (Latency):** Processing a book must complete in seconds using local CPU resources without external API dependencies.
*   **NFR 3.1.2 (Offline Capability):** The architecture uses only standard Python libraries and does not require network connectivity or external services.

### 3.2 Robustness and Error Handling
*   **NFR 3.2.1 (Validation):** The system must gracefully handle extraction edge cases and return sensible defaults when no features are found.
*   **NFR 3.2.2 (Input Validation):** The system must validate the input `book.md` file for basic structural integrity before processing begins.

## 4. Technical Design & Architecture (The "Blueprint")

### 4.1 Data Pipeline Flow
The overall process is designed as a linear, heuristic-driven pipeline:

1.  **Stage 1: Ingestion:** Read `book.md` and validate structure.
2.  **Stage 2: Pre-processing & Segmentation:** Parse Markdown to identify chapter boundaries using heading pattern matching. Output: List of structured chapter objects.
3.  **Stage 3: Feature Extraction:** For each chapter, apply regex patterns, dictionary lookups, and statistical analysis to identify glossary terms, idioms, and phrasal verbs.
4.  **Stage 4: Data Structuring:** Format extracted features into consistent Markdown tables with appropriate headers and sections.
5.  **Stage 5: Output Generation:** Write individual chapter files to `outputs/` directory.

### 4.2 Implementation Approach
This system uses **local rule-based heuristics** rather than external LLM agents:

*   **Glossary Extraction:** Uses regex patterns (`\b[a-zA-Z]{4,}\b`) combined with stop-word filtering and word frequency analysis to identify uncommon vocabulary words.
*   **Idiom Detection:** Uses exact string matching against predefined idiom dictionaries (both phrasal verbs and common idioms).
*   **Difficulty Scoring:** Analyzes average word length and text complexity metrics to assign difficulty levels.
*   **Definition Generation:** Creates contextual definitions based on surrounding sentence extraction and term classification.

### 4.3 Technology Stack
*   **Core Language:** Python 3.x with standard library only (no external API dependencies).
*   **Regex Processing:** Built-in `re` module for pattern matching.
*   **File Operations:** Standard file I/O using `pathlib` and `os` modules.
*   **JSON Handling:** Built-in `json` module for data structure validation.

## 5. Verification Plan

To verify this specification is met:
1.  **Unit Tests:** Develop unit tests to ensure the Segmentation logic correctly identifies chapter boundaries (testing `FR 2.1.1`).
2.  **Integration Test:** Run an end-to-end test with a known `book.md` input and validate that the generated `outputs/chapter_{ID}.md` files match the required structure defined in `FR 2.3.2`.
3.  **Error Handling Test:** Verify that the system handles malformed input gracefully without crashing.
