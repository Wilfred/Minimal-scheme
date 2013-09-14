from .base import name_function
from utils import check_argument_number
from data_types import (Cons, Nil, Boolean)


@name_function('car')
def car(arguments):
    # TODO: check type as well as arity
    check_argument_number('car', arguments, 1)

    list_given = arguments[0]

    return list_given[0]


@name_function('cdr')
def cdr(arguments):
    # TODO: check type as well as arity
    check_argument_number('cdr', arguments, 1)

    list_given = arguments[0]
    return list_given.tail


@name_function('cons')
def cons(arguments):
    # TODO: check type as well as arity
    check_argument_number('cons', arguments, 2, 2)

    return Cons(arguments[0], arguments[1])


@name_function('null?')
def is_null(arguments):
    check_argument_number('null?', arguments, 1, 1)

    if isinstance(arguments[0], Nil):
        return Boolean(True)

    return Boolean(False)

@name_function('pair?')
def pair(arguments):
    check_argument_number('pair?', arguments, 1, 1)

    if isinstance(arguments[0], Cons):
        return Boolean(True)

    return Boolean(False)


