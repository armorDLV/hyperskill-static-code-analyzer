"""Parsing of command line arguments."""

import argparse


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_or_file', help='path to *.py file or directory containing *.py files', type=str)
    return parser.parse_args()


CONSOLE_ARGS = _parse_arguments()

# optional: delete function after use to prevent calling from other place
del _parse_arguments
