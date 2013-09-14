from .base import name_function
from utils import check_argument_number
from data_types import Vector, Boolean


@name_function('vector?')
def is_vector(arguments):
    check_argument_number('make-vector', arguments, 1, 1)

    if isinstance(arguments[0], Vector):
        return Boolean(True)

    return Boolean(False)


# todo: initialisation argument
@name_function('make-vector')
def make_vector(arguments):
    check_argument_number('make-vector', arguments, 1, 1)

    # todo: type check this is an integer
    vector_length = arguments[0].value
    return Vector(vector_length)
