from ghbq.sample import main
from util import fileread
from util import filewrite
from util import patch_argv


def test_sample():
    filewrite('sample.csv', """
    foo/bar:refs/heads/master:foo
    foo/bar:refs/heads/master:bar
    """)

    with patch_argv('sample.csv', 1):
        main()
    assert fileread('sample.1.csv').count('\n') == 1
