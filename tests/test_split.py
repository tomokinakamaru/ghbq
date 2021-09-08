from ghbq.split import main
from util import fileread
from util import filewrite
from util import patch_argv


def test_sample():
    filewrite('sample.csv', """
    foo/bar:refs/heads/master:foo
    foo/bar:refs/heads/master:bar
    """)

    with patch_argv('sample.csv'):
        main()
    assert fileread('sample.a.csv').count('\n') == 1
    assert fileread('sample.b.csv').count('\n') == 1
