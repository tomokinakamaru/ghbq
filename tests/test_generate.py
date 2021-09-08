from ghbq.generate import main
from textwrap import dedent
from util import patch_argv


def test_generate(capfd):
    with patch_argv('^foo$'):
        main()

    out, _ = capfd.readouterr()
    assert out == dedent("""\
    # Run this on https://console.cloud.google.com/bigquery
    SELECT DISTINCT CONCAT(repo_name, ":", ref, ":", path)
    FROM bigquery-public-data.github_repos.sample_files -- For testing
    -- FROM bigquery-public-data.github_repos.files -- For production
    WHERE REGEXP_CONTAINS(path, r"^foo$")
    """)


def test_branch(capfd):
    with patch_argv('^foo$', '-b', 'bar'):
        main()

    out, _ = capfd.readouterr()
    assert out == dedent("""\
    # Run this on https://console.cloud.google.com/bigquery
    SELECT DISTINCT CONCAT(repo_name, ":", ref, ":", path)
    FROM bigquery-public-data.github_repos.sample_files -- For testing
    -- FROM bigquery-public-data.github_repos.files -- For production
    WHERE ref = "refs/heads/bar" AND REGEXP_CONTAINS(path, r"^foo$")
    """)


def test_sample(capfd):
    with patch_argv('^foo$', '-s', 100):
        main()

    out, _ = capfd.readouterr()
    assert out == dedent("""\
    # Run this on https://console.cloud.google.com/bigquery
    SELECT DISTINCT CONCAT(repo_name, ":", ref, ":", path)
    FROM bigquery-public-data.github_repos.sample_files -- For testing
    -- FROM bigquery-public-data.github_repos.files -- For production
    WHERE REGEXP_CONTAINS(path, r"^foo$")
    ORDER BY RAND() LIMIT 100
    """)
