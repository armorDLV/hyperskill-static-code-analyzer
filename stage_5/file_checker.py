import ast
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
        self._tree = None
        self._error_dict = dict()
        self._nodes = None

    def check_errors(self):

        with open(self._file_path, 'r') as file:
            for self._line_number, line_string in enumerate(file, start=1):

                self._line = Line(line_string)

                if self._line.is_blank():
                    self._blank_lines_count += 1
                else:
                    self._check_errors_001_to_009()
                    self._blank_lines_count = 0

        with open(self._file_path, 'r') as file:
            self._tree = ast.parse(file.read())
            self._nodes = ast.walk(self._tree)
            self._check_errors_010_to_012()

        for error in self._error_dict.values():
            print(error)

    def _check_errors_001_to_009(self):
        if self._line.length > self.MAX_LINE_LENGTH:
            self._log_error('S001', f'Line is longer than {self.MAX_LINE_LENGTH} characters')

        if self._line.indent % self.INDENT_MODULUS != 0:
            self._log_error('S002', f'Indentation is not a multiple of {self.INDENT_MODULUS}')

        if self._line.statement.endswith(';'):
            self._log_error('S003', f'Unnecessary semicolon after a statement')

        if self._line.has_inline_comment() and self._line.comment_spacing < 2:
            self._log_error('S004', f'Less than two spaces before inline comment')

        if 'TODO' in self._line.comment.upper():
            self._log_error('S005', f'TODO found in line')

        if self._blank_lines_count > 2:
            self._log_error('S006', f'More than two blank lines preceding this line')

        if match := self._search_definition():
            keyword, separation, name = match.groups()

            if len(separation) > 1:
                self._log_error('S007', f'Too many spaces after "{keyword}"')

            if keyword == 'class':
                result = self._is_camel_case(name)
                if not result:
                    self._log_error('S008', f'Class name "{name}" should use CamelCase')

            if keyword == 'def':
                result = self._is_snake_case(name)
                if not result:
                    self._log_error('S009', f'Function name "{name}" should use snake_case')

    def _check_errors_010_to_012(self):
        for node in self._nodes:

            if isinstance(node, ast.FunctionDef):
                self._line_number = node.lineno

                arg_names = [arg.arg for arg in node.args.args]
                for arg_name in arg_names:
                    if not self._is_snake_case(arg_name):
                        self._log_error('S010', f'Argument name "{arg_name}" should be written in snake_case')

                defaults = {type(default).__name__ for default in node.args.defaults}
                defaults.discard('Constant')
                if defaults != set():
                    self._log_error('S012', f'The default argument value is mutable')

            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                targets = [assign.targets[0] for assign in node.body if isinstance(assign, ast.Assign)]

                if len(targets) > 0:
                    for target in targets:
                        if isinstance(target, ast.Name):
                            if not self._is_snake_case(target.id):
                                self._line_number = target.lineno
                                self._log_error('S011', f'Variable "{target.id}" should be written in snake_case')

    def _search_definition(self) -> re.Match | None:
        return re.search(r'\b(def|class)(\s+)(\w+)', self._line.statement)

    def _log_error(self, error_code: str, error_message: str):
        key = str(self._line_number).zfill(3) + error_code
        self._error_dict[key] = f'{self._file_path}: Line {self._line_number}: {error_code} {error_message}'

    @staticmethod
    def _is_camel_case(name: str):
        return bool(re.match(r'([A-Z][a-z\d]+)+$', name))

    @staticmethod
    def _is_snake_case(name: str):
        return bool(re.match(r'[_a-z]+', name))
