from utils import flatten_linked_list, len_linked_list
from errors import SchemeTypeError

built_ins = {}

# a decorator for giving a name to built-in
def name_function(function_name):
    def name_function_decorator(function):
        built_ins[function_name] = function

    return name_function_decorator

@name_function('+')
def add_function(arguments):
    total = 0

    for argument in flatten_linked_list(arguments):
        if type(argument) == int:
            total += argument
        else:
            raise SchemeTypeError("Can't add something that isn't an integer.")
    return total


@name_function('*')
def multiply_function(arguments):
    product = 1

    for argument in flatten_linked_list(arguments):
        if type(argument) == int:
            product *= argument
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
        return -1 * head
    else:
        total = head

        for argument in flatten_linked_list(tail):
            total -= argument

        return total


@name_function('=')
def equality_function(arguments):
    if len_linked_list(arguments) < 2:
        raise SchemeTypeError("Equality test requires two arguments or more.")

    head, tail = arguments

    for argument in flatten_linked_list(tail):
        if argument != head:
            return False
    return True


@name_function('<')
def less_than(arguments):
    if len_linked_list(arguments) < 2:
        raise SchemeTypeError("Less than test requires at least two arguments.")

    flat_arguments = flatten_linked_list(arguments)

    for i in range(len(flat_arguments) - 1):
        if not flat_arguments[i] < flat_arguments[i+1]:
            return False

    return True


@name_function('>')
def greater_than(arguments):
    if len_linked_list(arguments) < 2:
        raise SchemeTypeError("Greater than test requires at least two arguments.")

    flat_arguments = flatten_linked_list(arguments)

    for i in range(len(flat_arguments) - 1):
        if not flat_arguments[i] > flat_arguments[i+1]:
            return False

    return True
