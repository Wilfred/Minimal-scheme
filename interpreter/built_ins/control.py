from .base import name_function
from utils import check_argument_number
from data_types import Boolean


@name_function('procedure?')
def is_procedure(arguments):
    check_argument_number('procedure?', arguments, 1, 1)

    if callable(arguments[0]):
        return Boolean(True)

    return Boolean(False)
