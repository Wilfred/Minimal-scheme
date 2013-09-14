from .base import name_function
from utils import check_argument_number


@name_function('display')
def display(arguments):
    check_argument_number('display', arguments, 1, 1)

    atom = arguments[0]
    print(atom.get_python_equivalent(), end='')

    return None
