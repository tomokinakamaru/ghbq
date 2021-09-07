from argparse import ArgumentParser
from argparse import HelpFormatter
from functools import update_wrapper


def arg(*args, **kwargs):
    def _(f):
        if isinstance(f, Command):
            f.arg(*args, **kwargs)
            return f
        c = Command(f)
        c.arg(*args, **kwargs)
        update_wrapper(c, f)
        return c
    return _


class Command(object):
    def __init__(self, func):
        self.parser = ArgumentParser(formatter_class=Formatter)
        self.func = func
        self.args = []

    def arg(self, *args, **kwargs):
        if args and args[0].startswith('--'):
            args = (f'-{args[0][2]}',) + args
        self.args.append((args, kwargs))

    def __call__(self):
        while self.args:
            args, kwargs = self.args.pop()
            self.parser.add_argument(*args, **kwargs)
        return self.func(self.parser.parse_args())


class Formatter(HelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, max_help_position=120, width=120)
