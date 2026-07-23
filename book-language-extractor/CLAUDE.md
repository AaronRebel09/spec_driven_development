<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan

## Project Overview
The `book-language-extractor` is a local heuristic-based tool that processes Markdown books and extracts linguistic features (glossary terms, idioms, phrasal verbs) for each chapter using pure Python with no external dependencies.

## Technology Stack
- **Language**: Python 3.x (standard library only)
- **Modules Used**: `re` (regex patterns), `json`, `os`, `pathlib`
- **No Dependencies**: Does not require external pip packages or API access

## Key Files
- `extractor.py`: Main pipeline - segmentation, extraction, and output generation
- `generate_chapters.py`: Utility for tracking missing chapter outputs
- `plan.md`: Implementation plan and architecture overview
- `tasks.md`: Detailed task breakdown with completion status
- `spec/`: Specification documents defining functional requirements

## Design Decisions
- **Local Processing**: All extraction performed locally, no network calls
- **Rule-Based**: Uses regex patterns and dictionary lookups rather than ML models
- **Offline Operation**: Works without internet connectivity
<!-- SPECKIT END -->
