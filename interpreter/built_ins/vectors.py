from .base import name_function
from utils import check_argument_number
from data_types import Vector, Boolean, Nil


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


@name_function('vector-ref')
def vector_ref(arguments):
    check_argument_number('vector-ref', arguments, 2, 2)

    vector = arguments[0]
    index = arguments[1].value

    return vector[index]


@name_function('vector-set!')
def vector_set(arguments):
    check_argument_number('vector-ref', arguments, 3, 3)

    vector = arguments[0]
    index = arguments[1].value
    new_value = arguments[2]

    vector[index] = new_value

    return Nil()
