from ghbq.sample import main
from util import argv
from util import fileread
from util import filewrite


def test_sample():
    filewrite('sample.csv', """
    foo/bar:refs/heads/master:foo
    foo/bar:refs/heads/master:bar
    """)

    with argv('sample.csv', 1):
        main()

    assert fileread('sample.1.csv').count('\n') == 1
