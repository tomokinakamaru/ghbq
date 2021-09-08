import sys
from textwrap import dedent
from unittest.mock import patch


def argv(*args):
    argv = sys.argv[:1] + list(map(str, args))
    return patch('argparse._sys.argv', argv)


def fileread(path):
    with open(path) as f:
        return f.read()


def filewrite(path, text):
    text = text.lstrip('\n')
    text = dedent(text).strip()
    with open(path, 'w') as f:
        print(text, file=f)
