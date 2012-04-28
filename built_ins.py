import math
from copy import copy

from errors import SchemeTypeError, InvalidArgument
from data_types import (Cons, Nil, String, Integer, Character, Boolean,
                        FloatingPoint, Number)
from utils import check_argument_number

built_ins = {}

# a decorator for giving a name to built-in
def name_function(function_name):
    def name_function_decorator(function):
        built_ins[function_name] = function

        # we return the function too, so we can use multiple decorators
        return function

    return name_function_decorator

@name_function('eq?')
@name_function('eqv?')
def test_equivalence(arguments):
    check_argument_number('eqv?', arguments, 2, 2)

    # __eq__ is defined on on Atom and Nil
    # and == on Cons just compares references, so we can just use a normal equality test
    if arguments[0] == arguments[1]:
        return Boolean(True)
    else:
        return Boolean(False)


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


@name_function('=')
def equality(arguments):

    for argument in arguments:
        if not isinstance(argument, Number):
            raise SchemeTypeError("Numerical equality test is only defined for numbers, "
                                  "you gave me %s." % argument.__class__)

        if argument != arguments[0]:
            return Boolean(False)

    return Boolean(True)


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
                              "you gave me %s." % argument.__class__)

    x1 = arguments[0].value
    return FloatingPoint(math.log(x1))


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


@name_function('char>?')
def char_greater_than(arguments):
    check_argument_number('char>?', arguments, 2, 2)

    if not isinstance(arguments[0], Character) or not isinstance(arguments[1], Character):
        raise SchemeTypeError("char>? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].__class__,
                                                arguments[1].__class__))

    if arguments[0].value > arguments[1].value:
        return Boolean(True)

    return Boolean(False)


@name_function('char<=?')
def char_less_or_equal(arguments):
    check_argument_number('char<=?', arguments, 2, 2)

    if not isinstance(arguments[0], Character) or not isinstance(arguments[1], Character):
        raise SchemeTypeError("char<=? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].__class__,
                                                arguments[1].__class__))

    if arguments[0].value <= arguments[1].value:
        return Boolean(True)

    return Boolean(False)


@name_function('char>=?')
def char_greater_or_equal(arguments):
    check_argument_number('char>=?', arguments, 2, 2)

    if not isinstance(arguments[0], Character) or not isinstance(arguments[1], Character):
        raise SchemeTypeError("char>=? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].__class__,
                                                arguments[1].__class__))

    if arguments[0].value >= arguments[1].value:
        return Boolean(True)

    return Boolean(False)


@name_function('string?')
def is_string(arguments):
    check_argument_number('string?', arguments, 1, 1)

    if isinstance(arguments[0], String):
        return Boolean(True)

    return Boolean(False)


@name_function('make-string')
def make_string(arguments):
    check_argument_number('make-string', arguments, 1, 2)

    string_length_atom = arguments[0]

    if not isinstance(string_length_atom, Integer):
        raise SchemeTypeError("String length must be an integer, "
                              "got %d." % string_length_atom.__class__)

    string_length = string_length_atom.value

    if string_length < 0:
        raise InvalidArgument("String length must be non-negative, "
                              "got %d." % string_length)

    if len(arguments) == 1:
        return String(' ' * string_length)

    else:
        repeated_character_atom = arguments[1]

        if not isinstance(repeated_character_atom, Character):
            raise SchemeTypeError("The second argument to make-string must be"
                                  " a character, got a %s." % repeated_character_atom.__class__)

        repeated_character = repeated_character_atom.value
        return String(repeated_character * string_length)


@name_function('string-length')
def string_length(arguments):
    check_argument_number('string_length', arguments, 1, 1)

    string_atom = arguments[0]
    if not isinstance(string_atom, String):
        raise SchemeTypeError("string-length takes a string as its argument, "
                              "not a %s." % string_atom.__class__)

    string_length = len(string_atom.value)
    return Integer(string_length)

@name_function('string-ref')
def string_ref(arguments):
    check_argument_number('string_length', arguments, 2, 2)

    string_atom = arguments[0]
    if not isinstance(string_atom, String):
        raise SchemeTypeError("string-ref takes a string as its first argument, "
                              "not a %s." % string_atom.__class__)

    char_index_atom = arguments[1]
    if not isinstance(char_index_atom, Integer):
        raise SchemeTypeError("string-ref takes an integer as its second argument, "
                              "not a %s." % char_index_atom.__class__)

    string = string_atom.value
    char_index = char_index_atom.value

    if char_index >= len(string):
        # FIXME: this will say 0--1 if string is ""
        raise InvalidArgument("String index out of bounds: index must be in"
                              " the range 0-%d, got %d." % (len(string) - 1, char_index))

    return Character(string[char_index])


@name_function('string-set!')
def string_set(arguments):
    check_argument_number('string_length', arguments, 3, 3)

    string_atom = arguments[0]
    if not isinstance(string_atom, String):
        raise SchemeTypeError("string-set! takes a string as its first argument, "
                              "not a %s." % string_atom.__class__)

    char_index_atom = arguments[1]
    if not isinstance(char_index_atom, Integer):
        raise SchemeTypeError("string-set! takes an integer as its second argument, "
                              "not a %s." % char_index_atom.__class__)

    replacement_char_atom = arguments[2]
    if not isinstance(replacement_char_atom, Character):
        raise SchemeTypeError("string-set! takes a character as its third argument, "
                              "not a %s." % replacement_char_atom.__class__)

    string = string_atom.value
    char_index = char_index_atom.value

    if char_index >= len(string):
        # FIXME: this will say 0--1 if string is ""
        raise InvalidArgument("String index out of bounds: index must be in"
                              " the range 0-%d, got %d." % (len(string) - 1, char_index))

    characters = list(string)
    characters[char_index] = replacement_char_atom.value
    new_string = "".join(characters)

    string_atom.value = new_string

    return None

@name_function('display')
def display(arguments):
    check_argument_number('display', arguments, 1, 1)

    atom = arguments[0]
    print(atom.get_python_equivalent(), end='')

    return None

@name_function('newline')
def newline(arguments):
    check_argument_number('newline', arguments, 0, 0)

    print("\n", end='')
