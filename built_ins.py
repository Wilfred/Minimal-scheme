from utils import flatten_linked_list, len_linked_list
from errors import SchemeTypeError
from parser import Atom

built_ins = {}

# a decorator for giving a name to built-in
def name_function(function_name):
    def name_function_decorator(function):
        built_ins[function_name] = function

    return name_function_decorator


@name_function('car')
def car_function(arguments):
    if len_linked_list(arguments) != 1:
        raise SchemeTypeError("car takes exactly one argument")

    first_argument, is_empty = arguments

    head, tail = first_argument
    return head


@name_function('cdr')
def cdr_function(arguments):
    if len_linked_list(arguments) != 1:
        raise SchemeTypeError("car takes exactly one argument")

    first_argument, is_empty = arguments

    head, tail = first_argument
    return tail


@name_function('+')
def add_function(arguments):
    total = Atom('INTEGER', 0)

    for argument in flatten_linked_list(arguments):
        if argument.type == "INTEGER":
            total.value += argument.value
        else:
            raise SchemeTypeError("Addition is only defined for integers, you gave me %s." % argument.type)
    return total


@name_function('*')
def multiply_function(arguments):
    product = Atom('INTEGER', 1)

    for argument in flatten_linked_list(arguments):
        if argument.type == 'INTEGER':
            product.value *= argument.value
        else:
            raise SchemeTypeError("Can't multiply something that isn't an integer.")
    return product


@name_function('-')
def subtract_function(arguments):
    if not arguments:
        raise SchemeTypeError("Subtract takes at least one argument")

    head, tail = arguments

    if not tail:
        # only one argument, we just negate it
        return Atom('INTEGER', -1 * head.value)
    else:
        total = Atom('INTEGER', head.value)

        for argument in flatten_linked_list(tail):
            total -= argument

        return total


@name_function('=')
def equality_function(arguments):
    if len_linked_list(arguments) < 2:
        raise SchemeTypeError("Equality test requires two arguments or more.")

    head, tail = arguments

    for argument in flatten_linked_list(tail):
        if argument.value != head.value:
            return Atom('BOOLEAN', False)

    return Atom('BOOLEAN', True)


@name_function('<')
def less_than(arguments):
    if len_linked_list(arguments) < 2:
        raise SchemeTypeError("Less than test requires at least two arguments.")

    flat_arguments = flatten_linked_list(arguments)

    for i in range(len(flat_arguments) - 1):
        if not flat_arguments[i].value < flat_arguments[i+1].value:
            return Atom('BOOLEAN', False)

    return Atom('BOOLEAN', True)


@name_function('>')
def greater_than(arguments):
    if len_linked_list(arguments) < 2:
        raise SchemeTypeError("Greater than test requires at least two arguments.")

    flat_arguments = flatten_linked_list(arguments)

    for i in range(len(flat_arguments) - 1):
        if not flat_arguments[i].value > flat_arguments[i+1].value:
            return Atom('BOOLEAN', False)

    return Atom('BOOLEAN', True)

@name_function('/')
def divide(arguments):
    # TODO: support exact fractions
    # TODO: return integer if all arguments were integers and result is whole number
    if not arguments:
        raise SchemeTypeError("Division atkes at least on argument.")

    head, tail = arguments

    if tail is None:
        return Atom('FLOATING_POINT', 1 / head.value)
    else:
        result = Atom('FLOATING_POINT', head.value)

        for argument in flatten_linked_list(tail):
            result.value /= argument.value

        return result
