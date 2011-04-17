from errors import SchemeTypeError
from parser import Atom
from utils import safe_len, safe_iter

built_ins = {}

# a decorator for giving a name to built-in
def name_function(function_name):
    def name_function_decorator(function):
        built_ins[function_name] = function

    return name_function_decorator


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


@name_function('+')
def add(arguments):
    total = Atom('INTEGER', 0)

    for argument in safe_iter(arguments):
        if argument.type == "INTEGER":
            total.value += argument.value
        else:
            raise SchemeTypeError("Addition is only defined for integers, you gave me %s." % argument.type)
    return total


@name_function('*')
def multiply(arguments):
    product = Atom('INTEGER', 1)

    for argument in safe_iter(arguments):
        if argument.type == 'INTEGER':
            product.value *= argument.value
        else:
            raise SchemeTypeError("Can't multiply something that isn't an integer.")
    return product


@name_function('-')
def subtract(arguments):
    if not arguments:
        raise SchemeTypeError("Subtract takes at least one argument")

    if not arguments.tail:
        # only one argument, we just negate it
        return Atom('INTEGER', -1 * arguments.head.value)
    else:
        total = Atom('INTEGER', arguments.head.value)

        for argument in arguments.tail:
            total.value -= argument.value

        return total


@name_function('=')
def equality(arguments):
    if safe_len(arguments) < 2:
        raise SchemeTypeError("Equality test requires two arguments or more.")

    for argument in arguments.tail:
        if argument.value != arguments.head.value:
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
