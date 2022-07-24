"""Simple Python code line model.

    Expressed using Python lexical notation: https://docs.python.org/3/reference/introduction.html#notation

    line ::= [indentation] [statement] [comment_spacing] [#] [comment]
        indentation ::= any number of whitespace characters before the first non-white character
        statement ::= python code string
        comment_spacing ::= any number of whitespace characters after the statement [and before the #]
        comment ::= the string after the #

    Trailing spaces at the end of the line are ignored.

    Examples:
        Blank line:
            line = '    '
                indentation = ''
                statement = ''
                comment_spacing = ''
                comment = ''

        Comment line:
            line = '  # The comment symbol in Python is #    '
                indentation = '  '
                statement = ''
                comment_spacing = ''
                comment = ' The comment symbol in Python is #'

        Code line:
            line = '    def f(x: int) -> int:  '
                indentation = '    '
                statement = 'def f(x: int) -> int:'
                comment_spacing = ''
                comment = ' The comment symbol in Python is #'

        Code line with inline comment
            line = '    def f(x: int) -> int:   # Inline comment '
                indentation = '    '
                statement = 'def f(x: int) -> int:'
                comment_spacing = '   '
                comment = ' Inline comment'
"""

from dataclasses import dataclass, field


@dataclass
class Line:
    """Representation of a python code line using the model defined in the module docstring.

    Attributes:
        length: Integer count of the number of characters in the line
        indent: Integer count of the number of whitespace characters in the indentation
        statement: A string containing the python code
        comment_spacing: Integer count of the number of spaces between the statement and the comment symbol #
        comment: A string containing the string after the first #
    """

    _text: str = field(repr=False)

    length: int = field(default=0, init=False)
    indent: int = field(default=0, init=False)
    statement: str = field(default='', init=False)
    comment_spacing: int = field(default=0, init=False)
    comment: str = field(default='', init=False)

    def __post_init__(self):
        if not self.is_blank():
            self._get_components()

    def is_blank(self) -> bool:
        """Returns true when the line only contains whitespace characters"""
        return self._text.strip() == ''

    def has_inline_comment(self) -> bool:
        """Returns true when the line has an inline comment"""
        return bool(self.statement) and self._has_comment()

    def _has_comment(self) -> bool:
        """Returns true when the line only contains the comment symbol '#'"""
        return self._text.find('#') >= 0

    def _get_components(self):

        self._text = self._text.rstrip()  # Ignore trailing spaces
        self.length = len(self._text)

        self.indent = self.length - len(self._text.lstrip())

        auxiliary_list = self._text.split('#', maxsplit=1)
        self.statement = auxiliary_list[0].strip()

        if self.statement:
            self.comment_spacing = len(auxiliary_list[0]) - len(auxiliary_list[0].rstrip())

        if len(auxiliary_list) > 1:
            self.comment = auxiliary_list[1]
