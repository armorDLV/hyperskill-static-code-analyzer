from os import listdir
from os.path import isdir, join

from console_args import CONSOLE_ARGS
from file_checker import FileChecker

if __name__ == '__main__':
    DEBUG = False

    if DEBUG:
        path = '../test/this_stage/test_9.py'
    else:
        path = CONSOLE_ARGS.dir_or_file

    if isdir(path):
        python_files = sorted([file for file in listdir(path) if file.endswith('.py')])

        for python_file in python_files:
            file_path = join(path, python_file)
            FileChecker(file_path).check_errors()

    else:
        FileChecker(path).check_errors()
