from .base import define_built_in
from utils import check_argument_number


@define_built_in('display')
def display(arguments):
    check_argument_number('display', arguments, 1, 1)

    atom = arguments[0]
    print(atom.get_python_equivalent(), end='')

    return None
