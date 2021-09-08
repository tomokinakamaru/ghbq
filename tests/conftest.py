from os import chdir
from os import getcwd
from os import mkdir
from pytest import fixture
from shutil import rmtree


@fixture(autouse=True, scope='function')
def fixture(request):
    tmp = f'{request.node.module.__name__}.{request.node.name}'
    cwd = getcwd()
    mkdir(tmp)
    chdir(tmp)
    yield
    chdir(cwd)
    rmtree(tmp)
