from .base import name_function
from utils import check_argument_number

from data_types import (Boolean, Character)
from errors import SchemeTypeError


@name_function('char?')
def is_char(arguments):
    check_argument_number('char?', arguments, 1, 1)

    if isinstance(arguments[0], Character):
        return Boolean(True)

    return Boolean(False)


@name_function('char=?')
def char_equal(arguments):
    check_argument_number('char=?', arguments, 2, 2)

    if not isinstance(arguments[0], Character) or not isinstance(arguments[1], Character):
        raise SchemeTypeError("char=? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].__class__,
                                                arguments[1].__class__))

    if arguments[0].value == arguments[1].value:
        return Boolean(True)

    return Boolean(False)


@name_function('char<?')
def char_less_than(arguments):
    check_argument_number('char<?', arguments, 2, 2)

    if not isinstance(arguments[0], Character) or not isinstance(arguments[1], Character):
        raise SchemeTypeError("char<? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].__class__,
                                                arguments[1].__class__))

    if arguments[0].value < arguments[1].value:
        return Boolean(True)

    return Boolean(False)


