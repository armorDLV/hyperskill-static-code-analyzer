import unittest
from unittest import TestCase

from line import Line


class TestLine(TestCase):

    def test_blank(self):
        line = Line('    ')
        self.assertFalse(line.has_inline_comment())
        self.assertEqual(line.length, 0)
        self.assertEqual(line.indent, 0)
        self.assertEqual(line.statement, '')
        self.assertEqual(line.comment_spacing, 0)
        self.assertEqual(line.comment, '')

    def test_comment_only(self):
        line = Line('  # The comment symbol in Python is #    ')
        self.assertFalse(line.has_inline_comment())
        self.assertEqual(line.length, 37)
        self.assertEqual(line.indent, 2)
        self.assertEqual(line.statement, '')
        self.assertEqual(line.comment_spacing, 0)
        self.assertEqual(line.comment, ' The comment symbol in Python is #')

    def test_empty_comment(self):
        line = Line('  #  ')
        self.assertFalse(line.has_inline_comment())
        self.assertEqual(line.length, 3)
        self.assertEqual(line.indent, 2)
        self.assertEqual(line.statement, '')
        self.assertEqual(line.comment_spacing, 0)
        self.assertEqual(line.comment, '')

    def test_code_only(self):
        line = Line('    def f(x: int) -> int:  ')
        self.assertFalse(line.has_inline_comment())
        self.assertEqual(line.length, 25)
        self.assertEqual(line.indent, 4)
        self.assertEqual(line.statement, 'def f(x: int) -> int:')
        self.assertEqual(line.comment_spacing, 0)
        self.assertEqual(line.comment, '')

    def test_code_and_comment_line(self):
        line = Line('    def f(x: int) -> int:   # Inline comment ')
        self.assertTrue(line.has_inline_comment())
        self.assertEqual(line.length, 44)
        self.assertEqual(line.indent, 4)
        self.assertEqual(line.statement, 'def f(x: int) -> int:')
        self.assertEqual(line.comment_spacing, 3)
        self.assertEqual(line.comment, ' Inline comment')

    def test_is_blank(self):
        line = Line('    ')
        self.assertTrue(line.is_blank())
        line = Line('something')
        self.assertFalse(line.is_blank())


if __name__ == '__main__':
    unittest.main()
