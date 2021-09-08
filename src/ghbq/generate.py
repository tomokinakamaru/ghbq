from textwrap import dedent
from .util import arg


@arg('regexp', help='regexp in query', metavar='<regexp>')
@arg('--branch', help='branch name', metavar='<name>')
@arg('--sample', help='sample size', metavar='<n>', type=int)
def main(args):
    print('# Run this on https://console.cloud.google.com/bigquery')
    print(build_query(args))


def build_query(args):
    where = build_where(args)
    order = build_order(args)
    query = f"""
    SELECT DISTINCT CONCAT(repo_name, ":", ref, ":", path)
    FROM bigquery-public-data.github_repos.sample_files -- For testing
    -- FROM bigquery-public-data.github_repos.files -- For production
    WHERE {where}
    {order}
    """
    return dedent(query.lstrip('\n')).strip()


def build_where(args):
    ws = build_where_ref(args), build_where_path(args)
    return ' AND '.join(w for w in ws if w)


def build_order(args):
    return f'ORDER BY RAND() LIMIT {args.sample}' if args.sample else ''


def build_where_ref(args):
    return f'ref = "refs/heads/{args.branch}"' if args.branch else ''


def build_where_path(args):
    return f'REGEXP_CONTAINS(path, r"{args.regexp}")'


if __name__ == '__main__':
    main()  # pragma: no cover
