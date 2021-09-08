from ghbq.split import main
from util import argv
from util import fileread
from util import filewrite


def test_split():
    filewrite('sample.csv', """
    foo/bar:refs/heads/master:foo
    foo/bar:refs/heads/master:bar
    """)

    with argv('sample.csv'):
        main()

    assert fileread('sample.a.csv').count('\n') == 1
    assert fileread('sample.b.csv').count('\n') == 1
