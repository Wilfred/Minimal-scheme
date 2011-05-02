from errors import SchemeTypeError, InvalidArgument
from parser import Atom, Cons
from utils import get_type, check_argument_number

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
        return Atom('BOOLEAN', True)
    else:
        return Atom('BOOLEAN', False)


@name_function('car')
def car(arguments):
    # TODO: check type as well as arity
    check_argument_number('car', arguments, 1)

    list_given = arguments[0]

    return list_given.head


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


@name_function('pair?')
def pair(arguments):
    check_argument_number('pair?', arguments, 1, 1)

    if isinstance(arguments[0], Cons):
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('rational?')
@name_function('real?')
@name_function('complex?')
@name_function('number?')
def number(arguments):
    check_argument_number('number?', arguments, 1, 1)

    if get_type(arguments[0]) in ['INTEGER', 'FLOATING_POINT']:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('exact?')
def exact(arguments):
    check_argument_number('exact?', arguments, 1, 1)

    if get_type(arguments[0]) == 'INTEGER':
        return Atom('BOOLEAN', True)
    elif get_type(arguments[0]) == 'FLOATING_POINT':
        return Atom('BOOLEAN', False)
    else:
        raise SchemeTypeError("exact? only takes integers or floating point "
                              "numbers as arguments, you gave me ""%s." % \
                                  len(arguments))

@name_function('inexact?')
def inexact(arguments):
    check_argument_number('inexact?', arguments, 1, 1)

    if get_type(arguments[0]) == 'FLOATING_POINT':
        return Atom('BOOLEAN', True)
    elif get_type(arguments[0]) == 'INTEGER':
        return Atom('BOOLEAN', False)
    else:
        raise SchemeTypeError("exact? only takes integers or floating point "
                              "numbers as arguments, you gave me ""%s." % \
                                  len(arguments))

@name_function('+')
def add(arguments):
    if not arguments:
        return Atom('INTEGER', 0)

    if get_type(arguments[0]) == "INTEGER":
        total = Atom('INTEGER', 0)
    elif get_type(arguments[0]) == "FLOATING_POINT":
        total = Atom('FLOATING_POINT', 0.0)

    for argument in arguments:
        if argument.type not in ['INTEGER', 'FLOATING_POINT']:
            raise SchemeTypeError("Addition is only defined for integers and "
                                  "floating point, you gave me %s." % argument.type)

        if get_type(total) == "INTEGER" and get_type(argument) == "FLOATING_POINT":
            total.type = "FLOATING_POINT"

        total.value += argument.value
    return total


@name_function('-')
def subtract(arguments):
    check_argument_number('-', arguments, 1)

    if len(arguments) == 1:
        if get_type(arguments[0]) not in ['INTEGER', 'FLOATING_POINT']:
            raise SchemeTypeError("Subtraction is only defined for integers and "
                                  "floating point, you gave me %s." % arguments[0].type)

        # only one argument, we just negate it
        return Atom(arguments[0].type, -1 * arguments[0].value)

    total = Atom(arguments[0].type, arguments[0].value)

    for argument in arguments.tail:
        if get_type(argument) not in ['INTEGER', 'FLOATING_POINT']:
            raise SchemeTypeError("Subtraction is only defined for integers and "
                                  "floating point, you gave me %s." % argument.type)

        if get_type(total) == "INTEGER" and get_type(argument) == "FLOATING_POINT":
            total.type = "FLOATING_POINT"

        total.value -= argument.value

    return total


@name_function('*')
def multiply(arguments):
    if not arguments:
        return Atom('INTEGER', 1)

    if get_type(arguments[0]) == "INTEGER":
        product = Atom('INTEGER', 1)
    elif get_type(arguments[0]) == "FLOATING_POINT":
        product = Atom('FLOATING_POINT', 1.0)

    for argument in arguments:
        if get_type(argument) not in ['INTEGER', 'FLOATING_POINT']:
            raise SchemeTypeError("Multiplication is only defined for integers and "
                                  "floating point, you gave me %s." % argument.type)

        if get_type(product) == "INTEGER" and get_type(argument) == "FLOATING_POINT":
            product.type = "FLOATING_POINT"

        product.value *= argument.value

    return product


@name_function('/')
def divide(arguments):
    # TODO: support exact fractions
    # TODO: return integer if all arguments were integers and result is whole number
    check_argument_number('/', arguments, 1)

    if len(arguments) == 1:
        return Atom('FLOATING_POINT', 1 / arguments.head.value)
    else:
        result = Atom('FLOATING_POINT', arguments.head.value)

        for argument in arguments.tail:
            result.value /= argument.value

        return result


@name_function('=')
def equality(arguments):

    for argument in arguments:
        if argument.type not in ['INTEGER', 'FLOATING_POINT']:
            raise SchemeTypeError("Numerical equality test is only defined "
                                  "for integers and floating point numbers, "
                                  "you gave me %s." % argument.type)

        if argument.value != arguments[0].value:
            return Atom('BOOLEAN', False)

    return Atom('BOOLEAN', True)


@name_function('<')
def less_than(arguments):
    check_argument_number('<', arguments, 2)

    for i in range(len(arguments) - 1):
        if not arguments[i].value < arguments[i+1].value:
            return Atom('BOOLEAN', False)

    return Atom('BOOLEAN', True)


@name_function('>')
def greater_than(arguments):
    check_argument_number('>', arguments, 2)

    for i in range(len(arguments) - 1):
        if not arguments[i].value > arguments[i+1].value:
            return Atom('BOOLEAN', False)

    return Atom('BOOLEAN', True)


@name_function('char?')
def is_char(arguments):
    check_argument_number('char?', arguments, 1, 1)

    if get_type(arguments[0]) == "CHARACTER":
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char=?')
def char_equal(arguments):
    check_argument_number('char=?', arguments, 2, 2)

    if get_type(arguments[0]) != "CHARACTER" or get_type(arguments[1]) != "CHARACTER":
        raise SchemeTypeError("char=? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].type, arguments[1].type))

    if arguments[0].value == arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char<?')
def char_less_than(arguments):
    check_argument_number('char<?', arguments, 2, 2)

    if get_type(arguments[0]) != "CHARACTER" or get_type(arguments[1]) != "CHARACTER":
        raise SchemeTypeError("char<? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].type, arguments[1].type))

    if arguments[0].value < arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char>?')
def char_greater_than(arguments):
    check_argument_number('char>?', arguments, 2, 2)

    if get_type(arguments[0]) != "CHARACTER" or get_type(arguments[1]) != "CHARACTER":
        raise SchemeTypeError("char>? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].type, arguments[1].type))

    if arguments[0].value > arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char<=?')
def char_less_or_equal(arguments):
    check_argument_number('char<=?', arguments, 2, 2)

    if get_type(arguments[0]) != "CHARACTER" or get_type(arguments[1]) != "CHARACTER":
        raise SchemeTypeError("char<=? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].type, arguments[1].type))

    if arguments[0].value <= arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char>=?')
def char_greater_or_equal(arguments):
    check_argument_number('char>=?', arguments, 2, 2)

    if get_type(arguments[0]) != "CHARACTER" or get_type(arguments[1]) != "CHARACTER":
        raise SchemeTypeError("char>=? takes only character arguments, got a "
                              "%s and a %s." % (get_type(arguments[0].type), get_type(arguments[1])))

    if arguments[0].value >= arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('string?')
def is_string(arguments):
    check_argument_number('string?', arguments, 1, 1)

    if get_type(arguments[0]) == 'STRING':
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('make-string')
def make_string(arguments):
    check_argument_number('make-string', arguments, 1, 2)

    string_length_atom = arguments[0]

    if get_type(string_length_atom) != "INTEGER":
        raise SchemeTypeError("String length must be an integer, "
                              "got %d." % get_type(string_length_atom))

    string_length = string_length_atom.value

    if string_length < 0:
        raise InvalidArgument("String length must be non-negative, "
                              "got %d." % string_length)

    if len(arguments) == 1:
        return Atom('STRING', ' ' * string_length)

    else:
        repeated_character_atom = arguments[1]

        if get_type(repeated_character_atom) != "CHARACTER":
            raise SchemeTypeError("The second argument to make-string must be"
                                  " a character, got a %s." % get_type(repeated_character_atom))

        repeated_character = repeated_character_atom.value
        return Atom('STRING', repeated_character * string_length)


@name_function('string-length')
def string_length(arguments):
    check_argument_number('string_length', arguments, 1, 1)

    string_atom = arguments[0]
    if get_type(string_atom) != 'STRING':
        raise SchemeTypeError("string-length takes a string as its argument, "
                              "not a %s." % get_type(string_atom))

    string_length = len(string_atom.value)
    return Atom('INTEGER', string_length)

@name_function('string-ref')
def string_ref(arguments):
    check_argument_number('string_length', arguments, 2, 2)

    string_atom = arguments[0]
    if get_type(string_atom) != 'STRING':
        raise SchemeTypeError("string-ref takes a string as its first argument, "
                              "not a %s." % get_type(string_atom))

    char_index_atom = arguments[1]
    if get_type(char_index_atom) != 'INTEGER':
        raise SchemeTypeError("string-ref takes an integer as its second argument, "
                              "not a %s." % get_type(char_index_atom))

    string = string_atom.value
    char_index = char_index_atom.value

    if char_index >= len(string):
        # FIXME: this will say 0--1 if string is ""
        raise InvalidArgument("String index out of bounds: index must be in"
                              " the range 0-%d, got %d." % (len(string) - 1, char_index))

    return Atom('CHARACTER', string[char_index])


@name_function('string-set!')
def string_set(arguments):
    check_argument_number('string_length', arguments, 3, 3)

    string_atom = arguments[0]
    if get_type(string_atom) != 'STRING':
        raise SchemeTypeError("string-set! takes a string as its first argument, "
                              "not a %s." % get_type(string_atom))

    char_index_atom = arguments[1]
    if get_type(char_index_atom) != 'INTEGER':
        raise SchemeTypeError("string-set! takes an integer as its second argument, "
                              "not a %s." % get_type(char_index_atom))

    replacement_char_atom = arguments[2]
    if get_type(replacement_char_atom) != 'CHARACTER':
        raise SchemeTypeError("string-set! takes a character as its third argument, "
                              "not a %s." % get_type(replacement_char_atom))

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
