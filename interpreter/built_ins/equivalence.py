from .base import define_built_in
from utils import check_argument_number

from data_types import (Cons, Atom, Boolean, Number)
from errors import SchemeTypeError


@define_built_in('eq?')
@define_built_in('eqv?')
def test_equivalence(arguments):
    check_argument_number('eqv?', arguments, 2, 2)

    if isinstance(arguments[0], Atom):
        # __eq__ is defined on Atom
        return Boolean(arguments[0] == arguments[1])
    if isinstance(arguments[0], Cons):
        # __eq__ on Cons is deep equality
        return Boolean(arguments[0] is arguments[1])
    else:
        # __eq__ is defined on Nil
        # todo: test vectors
        return Boolean(arguments[0] == arguments[1])


@define_built_in('=')
def equality(arguments):

    for argument in arguments:
        if not isinstance(argument, Number):
            raise SchemeTypeError("Numerical equality test is only defined for numbers, "
                                  "you gave me %s." % argument.__class__)

        if argument != arguments[0]:
            return Boolean(False)

    return Boolean(True)


