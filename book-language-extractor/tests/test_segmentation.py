import unittest
from extractor import detect_chapter_boundaries

class TestSegmentation(unittest.TestCase):
    def test_basic_segmentation(self):
        content = """
# Chapter 01: Title 1
Content for chapter 1.

# Chapter 02: Title 2
Content for chapter 2.
        """
        chapters = detect_chapter_boundaries(content)
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0][2], "Title 1")
        self.assertEqual(chapters[1][2], "Title 2")

    def test_no_headers(self):
        content = "Just some content without any headers."
        chapters = detect_chapter_boundaries(content)
        self.assertEqual(len(chapters), 0)

    def test_complex_headers(self):
        content = """
# Chapter 03: Complex Title |
Some content.

## Chapter 04: Subtitle
More content.
        """
        chapters = detect_chapter_boundaries(content)
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0][2], "Complex Title")
        self.assertEqual(chapters[1][2], "Subtitle")

if __name__ == '__main__':
    unittest.main()
