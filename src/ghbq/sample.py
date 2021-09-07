from os.path import splitext
from random import seed
from .util import arg
from .util import FileList


@arg('path', help='path to file list', metavar='<path>')
@arg('size', help='sample size', metavar='<n>', type=int)
@arg('--random', help='random seed', metavar='<n>', type=int)
def main(args):
    seed(args.random)
    name, ext = splitext(args.path)
    f = FileList.load(args.path).sample(args.size)
    f.save(f'{name}.{args.size}{ext}')
