from atomicwrites import atomic_write
from os.path import join
from random import sample


class FileList(object):
    @classmethod
    def load(cls, path):
        return cls(read(path))

    def __init__(self, lines):
        self.lines = tuple(lines)

    def __iter__(self):
        for line in self.lines:
            yield parse(line)

    def sample(self, n):
        return FileList(sample(self.lines, n))

    def split(self):
        m = len(self.lines) // 2
        return FileList(self.lines[:m]), FileList(self.lines[m:])

    def save(self, path):
        with atomic_write(path) as f:
            f.writelines(self.lines)


def read(path):
    with open(path) as f:
        for line in f:
            if 1 < line.count(':'):
                yield line


def parse(line):
    repo, ref, path = line.strip().split(':', 2)
    user, name = repo.split('/')
    branch = ref.split('/')[-1]
    return join(user, name, branch, path)
