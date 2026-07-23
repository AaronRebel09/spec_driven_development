# Tasks: Book Language Extractor - Local Implementation

**Input**: Design documents from `/specs/book-language-extraction/` (deprecated)

**Current Status**: Implementation Complete - Uses local rule-based extraction

## Phase 1: Core Segmentation (COMPLETED)

### Task 1.1: Chapter Boundary Detection
**Description**: Implement regex-based chapter boundary detection using Markdown heading patterns.

- [x] T001 Create `detect_chapter_boundaries()` function in `extractor.py`
- [x] T002 Implement heading pattern matching for #, ##, ### headers
- [x] T003 Handle complex titles with subtitles and pipe separators
- [x] T004 Extract content between chapter boundaries (start/end positions)

### Task 1.2: Input Validation
**Description**: Validate book.md file exists and has basic structural integrity before processing.

- [x] T005 Create `validate_input()` function to check file existence
- [x] T006 Implement content validation (non-empty, has headers)
- [x] T007 Add warning for chapter count mismatch vs expected chapters

## Phase 2: Local Feature Extraction (COMPLETED)

### Task 2.1: Glossary Extraction
**Description**: Implement rule-based glossary extraction using regex patterns and frequency analysis.

- [x] T001 Create `LocalExtractor` class with idiom pattern dictionary
- [x] T002 Implement word frequency extraction (4+ letter words, non-stopwords)
- [x] T003 Add context sentence extraction for each glossary term
- [x] T004 Implement deduplication by term name

### Task 2.2: Idiom and Phrasal Verb Detection
**Description**: Add dictionary-based idiom detection using exact string matching.

- [x] T005 Create idiom_patterns list with common phrasal verbs
- [x] T006 Create idiom_list with predefined idioms and meanings
- [x] T007 Implement case-insensitive matching in chapter content
- [x] T008 Add example sentence extraction for each detected idiom

### Task 2.3: Difficulty Scoring
**Description**: Assign difficulty levels based on text complexity metrics.

- [x] T001 Implement word length analysis (average character count)
- [x] T002 Calculate difficulty score: Low/Medium/High based on thresholds
- [x] T003 Handle unknown/unassigned scores with default "Medium"

### Task 2.4: Output Generation
**Description**: Format extracted features into Markdown tables for each chapter.

- [x] T001 Create `generate_chapter_markdown()` function
- [x] T002 Implement glossary table with Word/POS/Meaning/Spanish/Example/Difficulty
- [x] T003 Add Phrasal Verbs and Idioms tables
- [x] T004 Include Review section with key vocabulary summary

### Task 2.5: Chunking Support
**Description**: Handle content larger than processing limits by intelligent chunking.

- [x] T001 Create `chunk_content()` utility function
- [x] T002 Implement sentence-boundary splitting (periods/exclamation marks)
- [x] T003 Preserve paragraph boundaries during chunking
- [x] T004 Add chunk metadata tracking for aggregation

## Phase 3: Output Validation (COMPLETED)

### Task 3.1: File Generation Verification
**Description**: Verify all expected output files are generated correctly.

- [x] T001 Implement `validate_output()` function
- [x] T002 Check file existence and non-empty status
- [x] T003 Verify required sections present in each file
- [x] T004 Generate validation report with pass/fail summary

### Task 3.2: Pipeline Integration
**Description**: Create pipeline orchestrator to run full extraction process.

- [x] T001 Create `LanguageExtractorPipeline` class
- [x] T002 Implement sequential chapter processing loop
- [x] T003 Add progress logging during extraction
- [x] T004 Handle errors gracefully per-chapter without stopping entire run

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1 (Segmentation)**: Foundation - detects chapters before any extraction
- **Phase 2 (Extraction)**: Uses segmentation output to process each chapter
- **Phase 3 (Validation)**: Runs after all chapters processed to verify completeness

### Within Phases
- Task 1.1 → Task 1.2: Validation runs after boundary detection
- Tasks 2.1-2.4 run in parallel as independent extraction features
- Task 2.5 is optional enhancement for long documents
- Tasks 3.1-3.2 validate after full pipeline execution

## Notes

- All code follows existing project structure and style in `extractor.py`
- No external LLM dependencies - uses only Python standard library
- Local rule-based approach provides deterministic, offline operation
- Unit tests in `tests/` verify segmentation and pipeline functionality
- Migration complete: no legacy agent or chunking code remains
