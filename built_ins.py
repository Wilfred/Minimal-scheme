from errors import SchemeTypeError
from parser import Atom, LinkedListNode
from utils import safe_len, safe_iter

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
    if safe_len(arguments) != 2:
        raise SchemeTypeError("Equivalence predicate takes two "
                              "arguments, received %d." % safe_len(arguments))

    # since we have defined __eq__ on Atom objects and == on
    # LinkedListNodes compares addresses, we can just use a normal equality test
    if arguments[0] == arguments[1]:
        return Atom('BOOLEAN', True)
    else:
        return Atom('BOOLEAN', False)


@name_function('car')
def car(arguments):
    if safe_len(arguments) != 1:
        raise SchemeTypeError("car takes exactly one argument")

    list_given = arguments[0]

    return list_given.head


@name_function('cdr')
def cdr(arguments):
    if safe_len(arguments) != 1:
        raise SchemeTypeError("cdr takes exactly one argument")

    list_given = arguments[0]

    return list_given.tail


@name_function('cons')
def cons(arguments):
    if safe_len(arguments) != 2:
        raise SchemeTypeError("cons takes exactly two arguments.")

    return LinkedListNode(arguments[0], arguments[1])


@name_function('pair?')
def pair(arguments):
    if safe_len(arguments) != 1:
        raise SchemeTypeError("pair? takes exactly one argument.")

    if hasattr(arguments[0], 'type'):
        # is an atom
        return Atom('BOOLEAN', False)
    elif not arguments[0]:
        # is an empty list
        return Atom('BOOLEAN', False)

    return Atom('BOOLEAN', True)


@name_function('+')
def add(arguments):
    if not arguments:
        return Atom('INTEGER', 0)

    if arguments[0].type == "INTEGER":
        total = Atom('INTEGER', 0)
    elif arguments[0].type == "FLOATING_POINT":
        total = Atom('FLOATING_POINT', 0.0)

    for argument in safe_iter(arguments):
        if argument.type not in ['INTEGER', 'FLOATING_POINT']:
            raise SchemeTypeError("Addition is only defined for integers and "
                                  "floating point, you gave me %s." % argument.type)

        if total.type == "INTEGER" and argument.type == "FLOATING_POINT":
            total.type = "FLOATING_POINT"

        total.value += argument.value
    return total


@name_function('-')
def subtract(arguments):
    if not arguments:
        raise SchemeTypeError("Subtract takes at least one argument.")

    if safe_len(arguments) == 1:
        if arguments[0].type not in ['INTEGER', 'FLOATING_POINT']:
            raise SchemeTypeError("Subtraction is only defined for integers and "
                                  "floating point, you gave me %s." % arguments[0].type)

        # only one argument, we just negate it
        return Atom(arguments[0].type, -1 * arguments[0].value)

    total = Atom(arguments[0].type, arguments[0].value)

    for argument in arguments.tail:
        if argument.type not in ['INTEGER', 'FLOATING_POINT']:
            raise SchemeTypeError("Subtraction is only defined for integers and "
                                  "floating point, you gave me %s." % argument.type)

        if total.type == "INTEGER" and argument.type == "FLOATING_POINT":
            total.type = "FLOATING_POINT"

        total.value -= argument.value

    return total


@name_function('*')
def multiply(arguments):
    if not arguments:
        return Atom('INTEGER', 1)

    if arguments[0].type == "INTEGER":
        product = Atom('INTEGER', 1)
    elif arguments[0].type == "FLOATING_POINT":
        product = Atom('FLOATING_POINT', 1.0)

    for argument in safe_iter(arguments):
        if argument.type not in ['INTEGER', 'FLOATING_POINT']:
            raise SchemeTypeError("Multiplication is only defined for integers and "
                                  "floating point, you gave me %s." % argument.type)

        if product.type == "INTEGER" and argument.type == "FLOATING_POINT":
            product.type = "FLOATING_POINT"

        product.value *= argument.value

    return product


@name_function('/')
def divide(arguments):
    # TODO: support exact fractions
    # TODO: return integer if all arguments were integers and result is whole number
    if not arguments:
        raise SchemeTypeError("Division requires at least one argument.")

    if arguments.tail is None:
        return Atom('FLOATING_POINT', 1 / arguments.head.value)
    else:
        result = Atom('FLOATING_POINT', arguments.head.value)

        for argument in arguments.tail:
            result.value /= argument.value

        return result


@name_function('=')
def equality(arguments):
    if safe_len(arguments) < 2:
        raise SchemeTypeError("Equality test requires two arguments or more, "
                              "you gave %d." % safe_len(arguments))

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
    if safe_len(arguments) < 2:
        raise SchemeTypeError("Less than test requires at least two arguments.")

    for i in range(safe_len(arguments) - 1):
        if not arguments[i].value < arguments[i+1].value:
            return Atom('BOOLEAN', False)

    return Atom('BOOLEAN', True)


@name_function('>')
def greater_than(arguments):
    if safe_len(arguments) < 2:
        raise SchemeTypeError("Greater than test requires at least two arguments.")

    for i in range(safe_len(arguments) - 1):
        if not arguments[i].value > arguments[i+1].value:
            return Atom('BOOLEAN', False)

    return Atom('BOOLEAN', True)


@name_function('char?')
def is_char(arguments):
    if safe_len(arguments) != 1:
        raise SchemeTypeError("char? takes exactly one argument.")

    if arguments[0].type == "CHARACTER":
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char=?')
def char_equal(arguments):
    if safe_len(arguments) != 2:
        raise SchemeTypeError("char=? takes exactly two arguments.")

    if arguments[0].type != "CHARACTER" or arguments[1].type != "CHARACTER":
        raise SchemeTypeError("char=? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].type, arguments[1].type))

    if arguments[0].value == arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char<?')
def char_less_than(arguments):
    if safe_len(arguments) != 2:
        raise SchemeTypeError("char<? takes exactly two arguments.")

    if arguments[0].type != "CHARACTER" or arguments[1].type != "CHARACTER":
        raise SchemeTypeError("char<? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].type, arguments[1].type))

    if arguments[0].value < arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char>?')
def char_greater_than(arguments):
    if safe_len(arguments) != 2:
        raise SchemeTypeError("char>? takes exactly two arguments.")

    if arguments[0].type != "CHARACTER" or arguments[1].type != "CHARACTER":
        raise SchemeTypeError("char>? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].type, arguments[1].type))

    if arguments[0].value > arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char<=?')
def char_less_or_equal(arguments):
    if safe_len(arguments) != 2:
        raise SchemeTypeError("char<=? takes exactly two arguments.")

    if arguments[0].type != "CHARACTER" or arguments[1].type != "CHARACTER":
        raise SchemeTypeError("char<=? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].type, arguments[1].type))

    if arguments[0].value <= arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)


@name_function('char>=?')
def char_greater_or_equal(arguments):
    if safe_len(arguments) != 2:
        raise SchemeTypeError("char>=? takes exactly two arguments.")

    if arguments[0].type != "CHARACTER" or arguments[1].type != "CHARACTER":
        raise SchemeTypeError("char>=? takes only character arguments, got a "
                              "%s and a %s." % (arguments[0].type, arguments[1].type))

    if arguments[0].value >= arguments[1].value:
        return Atom('BOOLEAN', True)

    return Atom('BOOLEAN', False)

