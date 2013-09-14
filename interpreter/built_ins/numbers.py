import math
from copy import copy

from .base import name_function
from utils import check_argument_number
from data_types import (Boolean, Number, Integer, FloatingPoint)
from errors import SchemeTypeError


@name_function('rational?')
@name_function('real?')
@name_function('complex?')
@name_function('number?')
def number(arguments):
    check_argument_number('number?', arguments, 1, 1)

    if isinstance(arguments[0], Number):
        return Boolean(True)

    return Boolean(False)


@name_function('exact?')
def exact(arguments):
    check_argument_number('exact?', arguments, 1, 1)

    if isinstance(arguments[0], Integer):
        return Boolean(True)
    elif isinstance(arguments[0], FloatingPoint):
        return Boolean(False)
    else:
        raise SchemeTypeError("exact? only takes integers or floating point "
                              "numbers as arguments, you gave me ""%s." % \
                                  len(arguments))

@name_function('inexact?')
def inexact(arguments):
    check_argument_number('inexact?', arguments, 1, 1)

    if isinstance(arguments[0], FloatingPoint):
        return Boolean(True)
    elif isinstance(arguments[0], Integer):
        return Boolean(False)
    else:
        raise SchemeTypeError("exact? only takes integers or floating point "
                              "numbers as arguments, you gave me ""%s." % \
                                  len(arguments))

@name_function('+')
def add(arguments):
    if not arguments:
        return Integer(0)

    if isinstance(arguments[0], Integer):
        total = Integer(0)
    elif isinstance(arguments[0], FloatingPoint):
        total = FloatingPoint(0.0)

    for argument in arguments:
        if not isinstance(argument, Number):
            raise SchemeTypeError("Addition is only defined for numbers, "
                                  "you gave me %s." % argument.__class__)

        # adding a float to an integer gives us a float
        if isinstance(total, Integer) and isinstance(argument, FloatingPoint):
            total = FloatingPoint(float(total.value))

        total.value += argument.value
    return total


@name_function('-')
def subtract(arguments):
    check_argument_number('-', arguments, 1)

    if len(arguments) == 1:
        # we just negate a single argument
        if isinstance(arguments[0], Integer):
            return Integer(-1 * arguments[0].value)
        elif isinstance(arguments[0], FloatingPoint):
            return FloatingPoint(-1 * arguments[0].value)
        else:
            raise SchemeTypeError("Subtraction is only defined for integers and "
                                  "floating point, you gave me %s." % arguments[0].__class__)

    total = copy(arguments[0])

    for argument in arguments.tail:
        if not isinstance(argument, Number):
            raise SchemeTypeError("Subtraction is only defined for numbers, "
                                  "you gave me %s." % argument.__class__)

        # subtracting a float from an integer gives us a float
        if isinstance(total, Integer) and isinstance(argument, FloatingPoint):
            total = FloatingPoint(float(total.value))

        total.value -= argument.value

    return total


@name_function('*')
def multiply(arguments):
    if not arguments:
        return Integer(1)

    if isinstance(arguments[0], Integer):
        product = Integer(1)

    elif isinstance(arguments[0], FloatingPoint):
        product = FloatingPoint(1.0)

    for argument in arguments:
        if not isinstance(argument, Number):
            raise SchemeTypeError("Multiplication is only defined for numbers, "
                                  "you gave me %s." % argument.__class__)

        if isinstance(product, Integer) and isinstance(argument, FloatingPoint):
            product = FloatingPoint(float(product.value))

        product.value *= argument.value

    return product


@name_function('/')
def divide(arguments):
    # TODO: support exact fractions
    # TODO: return integer if all arguments were integers and result is whole number
    check_argument_number('/', arguments, 1)

    if len(arguments) == 1:
        return FloatingPoint(1 / arguments[0].value)
    else:
        result = FloatingPoint(arguments[0].value)

        for argument in arguments.tail:
            result.value /= argument.value

        return result


@name_function('<')
def less_than(arguments):
    check_argument_number('<', arguments, 2)

    for i in range(len(arguments) - 1):
        if not arguments[i].value < arguments[i+1].value:
            return Boolean(False)

    return Boolean(True)


@name_function('<=')
def less_or_equal(arguments):
    check_argument_number('<=', arguments, 2)

    for i in range(len(arguments) - 1):
        if not arguments[i].value <= arguments[i+1].value:
            return Boolean(False)

    return Boolean(True)


@name_function('>')
def greater_than(arguments):
    check_argument_number('>', arguments, 2)

    for i in range(len(arguments) - 1):
        if not arguments[i].value > arguments[i+1].value:
            return Boolean(False)

    return Boolean(True)


@name_function('>=')
def greater_or_equal(arguments):
    check_argument_number('>=', arguments, 2)

    for i in range(len(arguments) - 1):
        if not arguments[i].value >= arguments[i+1].value:
            return Boolean(False)

    return Boolean(True)


@name_function('quotient')
def quotient(arguments):
    # integer division
    check_argument_number('quotient', arguments, 2, 2)

    if not isinstance(arguments[0], Integer) or not isinstance(arguments[1], Integer):
        raise SchemeTypeError("quotient is only defined for integers, "
                              "got %s and %s." % (arguments[0].__class__,
                                                  arguments[1].__class__))

    # Python's integer division floors, whereas Scheme rounds towards zero
    x1 = arguments[0].value
    x2 = arguments[1].value
    result = math.trunc(x1 / x2)

    return Integer(result)


@name_function('modulo')
def modulo(arguments):
    check_argument_number('modulo', arguments, 2, 2)

    if not isinstance(arguments[0], Integer) or not isinstance(arguments[1], Integer):
        raise SchemeTypeError("modulo is only defined for integers, "
                              "got %s and %s." % (arguments[0].__class__,
                                                  arguments[1].__class__))

    return Integer(arguments[0].value % arguments[1].value)


@name_function('remainder')
def remainder(arguments):
    check_argument_number('remainder', arguments, 2, 2)

    if not isinstance(arguments[0], Integer) or not isinstance(arguments[1], Integer):
        raise SchemeTypeError("remainder is only defined for integers, "
                              "got %s and %s." % (arguments[0].__class__,
                                                  arguments[1].__class__))

    # as with quotient, we can't use Python's integer division here because it floors rather than truncates
    x1 = arguments[0].value
    x2 = arguments[1].value
    value = x1 - (math.trunc(x1 / x2) * x2)

    return Integer(value)


@name_function('exp')
def exp(arguments):
    check_argument_number('exp', arguments, 1, 1)

    if arguments[0].__class__ not in [Integer, FloatingPoint]:
        raise SchemeTypeError("exp only takes integers or floats, "
                              "got %s" % arguments[0].__class__)

    x1 = arguments[0].value
    return FloatingPoint(math.exp(x1))


@name_function('log')
def log(arguments):
    check_argument_number('log', arguments, 1, 1)

    if not isinstance(arguments[0], Number):
        raise SchemeTypeError("Log is only defined for numbers, "
                              "you gave me %s." % arguments[0].__class__)

    x1 = arguments[0].value
    return FloatingPoint(math.log(x1))
