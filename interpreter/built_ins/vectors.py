from .base import name_function
from utils import check_argument_number
from data_types import Vector, Boolean, Nil, Integer


@name_function('vector?')
def is_vector(arguments):
    check_argument_number('make-vector', arguments, 1, 1)

    if isinstance(arguments[0], Vector):
        return Boolean(True)

    return Boolean(False)


@name_function('make-vector')
def make_vector(arguments):
    check_argument_number('make-vector', arguments, 1, 2)

    # todo: type check this is an integer
    vector_length = arguments[0].value

    vector = Vector(vector_length)

    # If we're given an initialisation value, use it.
    if len(arguments) == 2:
        init_value = arguments[1]
        for i in range(vector_length):
            vector[i] = init_value
    
    return vector


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


@name_function('vector-length')
def vector_length(arguments):
    check_argument_number('vector-length', arguments, 1, 1)

    # todo: check type
    vector = arguments[0]

    return Integer(len(vector))
