from os.path import splitext
from .util import arg
from .util import FileList


@arg('path', help='path to file list', metavar='<path>')
def main(args):
    name, ext = splitext(args.path)
    f1, f2 = FileList.load(args.path).split()
    f1.save(f'{name}.a{ext}')
    f2.save(f'{name}.b{ext}')


if __name__ == '__main__':
    main()  # pragma: no cover
