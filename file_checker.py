import re

from line import Line


class FileChecker:
    MAX_LINE_LENGTH = 79
    INDENT_MODULUS = 4
    MIN_COMMENT_SPACING = 2

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._line_number = 0
        self._line = None
        self._blank_lines_count = 0

    def check_errors(self):
        with open(self._file_path, 'r') as file:
            for self._line_number, line_string in enumerate(file):

                self._line = Line(line_string)

                if self._line.is_blank():
                    self._blank_lines_count += 1
                else:
                    self._check_line_errors()
                    self._blank_lines_count = 0

    def _check_line_errors(self):
        if self._line.length > self.MAX_LINE_LENGTH:
            self._print_error(f'S001 Line is longer than {self.MAX_LINE_LENGTH} characters')

        if self._line.indent % self.INDENT_MODULUS != 0:
            self._print_error(f'S002 Indentation is not a multiple of {self.INDENT_MODULUS}')

        if self._line.statement.endswith(';'):
            self._print_error(f'S003 Unnecessary semicolon after a statement')

        if self._line.has_inline_comment() and self._line.comment_spacing < 2:
            self._print_error(f'S004 Less than two spaces before inline comments')

        if 'TODO' in self._line.comment.upper():
            self._print_error(f'S005 TODO found in line')

        if self._blank_lines_count > 2:
            self._print_error(f'S006 More than two blank lines preceding this line')

        if match := self._search_definition():
            keyword, separation, name = match.groups()

            if len(separation) > 1:
                self._print_error(f'S007 Too many spaces after "{keyword}"')

            if keyword == 'class':
                result = self._is_camel_case(name)
                if not result:
                    self._print_error(f'S008 Class name "{name}" should use CamelCase')

            if keyword == 'def':
                result = self._is_snake_case(name)
                if not result:
                    self._print_error(f'S009 Function name "{name}" should use snake_case')

    def _search_definition(self) -> re.Match | None:
        return re.search(r'\b(def|class)(\s+)(\w+)', self._line.statement)

    def _print_error(self, error_message: str):
        print(f'{self._file_path}: Line {self._line_number + 1}: {error_message}')

    @staticmethod
    def _is_camel_case(name: str):
        return bool(re.match(r'([A-Z][a-z\d]+)+$', name))

    @staticmethod
    def _is_snake_case(name: str):
        return bool(re.match(r'[_a-z]+', name))
