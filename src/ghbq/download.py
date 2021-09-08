from atomicwrites import atomic_write
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
from hashlib import md5
from os import makedirs
from os.path import dirname
from os.path import exists
from os.path import join
from os.path import splitext
from progress.counter import Counter
from ratelimit import limits
from ratelimit import sleep_and_retry
from threading import Lock
from urllib.request import urlopen
from .util import arg
from .util import FileList


@arg('path', help='path to file list', metavar='<path>')
@arg('--limit', default=5, help='request rate limit', metavar='<n>', type=int)
@arg('--threads', help='number of threads', metavar='<n>', type=int)
def main(args):
    outdir = splitext(args.path)[0]
    counter = Counter('> ')
    executor = ThreadPoolExecutor(args.threads)
    with counter, executor:
        f = partial(try_download, outdir)
        f = limit_rate(f, args.limit)
        d = FileList.load(args.path)
        for _ in executor.map(f, d):
            counter.next()
            counter.update()


def try_download(outdir, key):
    try:
        download(outdir, key)
    except Exception as e:
        log(outdir, f'{key} {e}')


def download(outdir, key):
    dig = md5(key.encode('utf8')).hexdigest()
    dst = join(outdir, dig[0], dig[1], key)
    if exists(dst):
        return

    url = f'https://raw.githubusercontent.com/{key}'
    res = request(url)
    save(res, dst)


def request(url):
    with urlopen(url) as r:
        return r.read()


def save(data, path):
    mkdir(dirname(path))
    with atomic_open(path, 'wb') as f:
        f.write(data)


def log(outdir, msg):
    mkdir(outdir)
    time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = f'{outdir}.err'
    with lock, open(path, 'a') as f:
        f.write(f'{time} {msg}\n')


def limit_rate(f, n):
    return sleep_and_retry(limits(calls=n, period=1)(f))


def atomic_open(path, mode='w'):
    return atomic_write(path, mode=mode)


def mkdir(path):
    makedirs(path, exist_ok=True)


lock = Lock()


if __name__ == '__main__':
    main()  # pragma: no cover
