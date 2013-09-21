from .base import define_built_in
from utils import check_argument_number

from data_types import (Boolean, Number)
from errors import SchemeTypeError


@define_built_in('eq?')
@define_built_in('eqv?')
def test_equivalence(arguments):
    check_argument_number('eqv?', arguments, 2, 2)

    # __eq__ is defined on on Atom and Nil
    # and == on Cons just compares references, so we can just use a normal equality test
    if arguments[0] == arguments[1]:
        return Boolean(True)
    else:
        return Boolean(False)


@define_built_in('=')
def equality(arguments):

    for argument in arguments:
        if not isinstance(argument, Number):
            raise SchemeTypeError("Numerical equality test is only defined for numbers, "
                                  "you gave me %s." % argument.__class__)

        if argument != arguments[0]:
            return Boolean(False)

    return Boolean(True)


