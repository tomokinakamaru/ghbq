from ghbq.download import main
from re import match
from unittest.mock import MagicMock
from unittest.mock import patch
from util import argv
from util import fileread
from util import filewrite


def test_download():
    filewrite('sample.csv', 'foo/bar:refs/heads/master:foo')

    with argv('sample.csv'), urlopen(b'foo'):
        main()

    assert fileread('sample/d/d/foo/bar/master/foo') == 'foo'


def test_download_existing():
    filewrite('sample.csv', 'foo/bar:refs/heads/master:foo')

    with argv('sample.csv'), urlopen(b'foo'):
        main()
    with argv('sample.csv'), urlopen(None):
        main()

    assert fileread('sample/d/d/foo/bar/master/foo') == 'foo'


def test_error():
    filewrite('sample.csv', 'foo/bar:refs/heads/master:foo')

    with argv('sample.csv'), urlopen(None):
        main()

    assert match(
        r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2} foo/bar/master/foo'
        " a bytes-like object is required, not 'NoneType'",
        fileread('sample.err')
    )


def urlopen(text):
    mock = MagicMock()
    mock.read.return_value = text
    mock.__enter__.return_value = mock
    return patch('ghbq.download.urlopen', lambda _: mock)
