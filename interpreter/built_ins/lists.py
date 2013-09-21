from .base import define_built_in
from utils import check_argument_number
from data_types import (Cons, Nil, Boolean)


@define_built_in('car')
def car(arguments):
    # TODO: check type as well as arity
    check_argument_number('car', arguments, 1)

    list_given = arguments[0]

    return list_given[0]


@define_built_in('cdr')
def cdr(arguments):
    # TODO: check type as well as arity
    check_argument_number('cdr', arguments, 1, 1)

    list_given = arguments[0]
    return list_given.tail


@define_built_in('set-car!')
def set_car(arguments):
    # TODO: check type as well as arity
    check_argument_number('set-car!', arguments, 2, 2)

    list_given = arguments[0]
    list_given.head = arguments[1]

    return Nil()


@define_built_in('cons')
def cons(arguments):
    # TODO: check type as well as arity
    check_argument_number('cons', arguments, 2, 2)

    return Cons(arguments[0], arguments[1])


@define_built_in('pair?')
def pair(arguments):
    check_argument_number('pair?', arguments, 1, 1)

    if isinstance(arguments[0], Cons):
        return Boolean(True)

    return Boolean(False)


