# Verification Plan: Book Language Extractor

This plan outlines the verification steps to ensure the `book-language-extractor` meets all requirements defined in `spec/book-language-extractor_spec.md`.

## 1. Unit Testing (Segmentation)
- **Test Case 1.1:** Verify correct identification of Markdown headers (`#`, `##`, `###`) as chapter boundaries using regex pattern matching.
- **Test Case 1.2:** Verify that blank lines between headers are correctly handled (not included in content).
- **Test Case 1.3:** Verify that segmentation handles chapters with complex titles, sub-chapters, and numbering variations.

## 2. Integration Testing (End-to-End)
- **Test Case 2.1:** Provide a sample `book.md` and verify that `outputs/` contains the expected number of `.md` files.
- **Test Case 2.2:** Verify that each output file contains the required sections: Glossary, Phrasal Verbs, Idioms, and Review.
- **Test Case 2.3:** Verify that the `difficulty_score` is consistently applied based on text complexity metrics.
- **Test Case 2.4:** Verify that glossary terms are extracted correctly without duplicates.

## 3. Feature Validation
- **Test Case 3.1:** Verify idiom detection matches predefined dictionary entries in source text.
- **Test Case 3.2:** Verify that unknown words are excluded (stop-word filtering works).
- **Test Case 3.3:** Verify that context sentences are extracted accurately for glossary terms.

## 4. Robustness & Error Handling
- **Test Case 4.1:** Provide malformed `book.md` and verify the pipeline returns a clear validation error.
- **Test Case 4.2:** Test with very short chapters (single sentence) to ensure no crashes.
- **Test Case 4.3:** Test with non-standard chapter headings to verify graceful fallback.

## 5. Performance & Scalability
- **Test Case 5.1:** Measure processing time for a 10,000-word sample (should complete in seconds).
- **Test Case 5.2:** Verify processing completes without external API dependencies or network calls.
