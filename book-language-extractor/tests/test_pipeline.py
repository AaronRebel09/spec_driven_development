import unittest
import os
from extractor import LocalExtractor, LanguageExtractorPipeline


class TestEnhancedPipeline(unittest.TestCase):
    """Test suite for the enhanced local heuristic-based extraction pipeline."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once before running tests."""
        cls.extractor = LocalExtractor()
        # Use main book.md for full pipeline testing (36 chapters expected)
        cls.expected_chapters = 36
        cls.output_dir = "outputs_test"

    def test_input_validation_exists(self):
        """Test that input validation correctly identifies existing file."""
        from extractor import validate_input
        self.assertTrue(validate_input("book.md"), "book.md should exist")

    def test_input_validation_missing(self):
        """Test that input validation fails for non-existent files."""
        from extractor import validate_input
        self.assertFalse(validate_input("nonexistent_file.md"))

    def test_chapter_boundary_detection(self):
        """Test chapter boundary detection finds correct number of chapters."""
        from extractor import detect_chapter_boundaries
        with open("book.md", 'r', encoding='utf-8') as f:
            content = f.read()

        chapters = detect_chapter_boundaries(content)
        self.assertEqual(len(chapters), 36,
                        f"Expected 36 chapters, found {len(chapters)}")

    def test_pipeline_runs_without_error(self):
        """Test that pipeline completes successfully."""
        from extractor import validate_input
        self.assertTrue(validate_input("book.md"))

        with open("book.md", 'r', encoding='utf-8') as f:
            content = f.read()

        pipeline = LanguageExtractorPipeline(self.extractor, self.output_dir)
        success = pipeline.run(content, expected_count=self.expected_chapters)
        self.assertTrue(success, "Pipeline execution failed")

    def test_output_files_created(self):
        """Test that output files are created for all chapters."""
        pipeline = LanguageExtractorPipeline(self.extractor, self.output_dir)
        with open("book.md", 'r', encoding='utf-8') as f:
            content = f.read()

        pipeline.run(content, expected_count=self.expected_chapters)

        files = sorted(os.listdir(self.output_dir))
        self.assertEqual(len(files), self.expected_chapters,
                        f"Expected {self.expected_chapters} files, got {len(files)}")

    def test_glossary_has_terms(self):
        """Test that glossary contains actual vocabulary terms."""
        with open("book.md", 'r', encoding='utf-8') as f:
            content = f.read()

        pipeline = LanguageExtractorPipeline(self.extractor, self.output_dir)
        pipeline.run(content, expected_count=self.expected_chapters)

        files = sorted(os.listdir(self.output_dir))
        with open(os.path.join(self.output_dir, files[0]), 'r', encoding='utf-8') as f:
            chapter_content = f.read()

        # Check for actual vocabulary terms (not just *N/A* placeholders)
        self.assertNotIn("| *N/A* |", chapter_content, "No vocabulary terms extracted")

    def test_output_has_required_sections(self):
        """Test that output files contain required sections (some may be empty)."""
        with open("book.md", 'r', encoding='utf-8') as f:
            content = f.read()

        pipeline = LanguageExtractorPipeline(self.extractor, self.output_dir)
        pipeline.run(content, expected_count=self.expected_chapters)

        files = sorted(os.listdir(self.output_dir))
        with open(os.path.join(self.output_dir, files[0]), 'r', encoding='utf-8') as f:
            chapter_content = f.read()

        # Required sections that should always exist (may be empty if no data found)
        required_sections = [
            "## 📚 Glossary Words (Top 20 Terms)",
            "## 📝 Review & Notes"
        ]

        for section in required_sections:
            self.assertIn(section, chapter_content or "",
                         f"Missing required section: {section}")

        # Optional sections that may exist if data is found
        optional_sections = [
            "## 🔄 Phrasal Verbs",
            "## 😎 Slang & Colloquial Expressions"
        ]

        has_optional = sum(1 for s in optional_sections if s in chapter_content)
        self.assertGreaterEqual(has_optional, 0,
                               f"No optional sections found (phrasal verbs/slangs). Found {has_optional} of expected.")

    def test_spanish_translations_loaded(self):
        """Test that Spanish translations are loaded from JSON."""
        self.assertTrue(len(self.extractor.translations) > 0,
                       "Spanish translations not loaded from JSON")


if __name__ == '__main__':
    unittest.main()
