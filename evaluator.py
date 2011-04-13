from parser import parser, Atom


class InterpreterException(Exception):
    def __init__(self, message):
        self.message = message

class UndefinedVariable(InterpreterException):
    pass

class RedefinedVariable(InterpreterException):
    pass

class SchemeTypeError(InterpreterException):
    # 'TypeError' is a built-in Python exception
    pass


variables = {}

def eval_program(program):
    # a program is a linked list of s-expressions
    if not program:
        return

    parse_tree = parser.parse(program)

    head, tail = parse_tree
    result = eval_s_expression(head)

    while tail:
        head, tail = tail
        result = eval_s_expression(head)

    return result


def eval_s_expression(s_expression):
    if isinstance(s_expression, tuple):
        return eval_list(s_expression)
    else:
        return eval_atom(s_expression)


def eval_list(linked_list):
    head, tail = linked_list

    # find the function we are calling
    function = eval_s_expression(head)

    # atom evaluate to themselves:
    if not tail:
        return function

    # call it (we require the function to decide whether or not to
    # evalue the arguments)
    return function(tail)

def eval_atom(atom):
    if atom.type == 'NUMBER':
        return eval_number(atom.value)
    elif atom.type == 'SYMBOL':
        return eval_symbol(atom.value)
    elif atom.type == 'BOOLEAN':
        return eval_boolean(atom.value)

def eval_number(number_string):
    return int(number_string)

def eval_symbol(symbol_string):
    if symbol_string == '+':

        def add_function(arguments):
            total = 0

            arguments = map_linked_list(eval_s_expression, arguments)

            for argument in flatten_linked_list(arguments):
                if type(argument) == int:
                    total += argument
                else:
                    raise SchemeTypeError("Can't add something that isn't an integer.")
            return total

        return add_function

    elif symbol_string == '*':

        def multiply_function(arguments):
            product = 1

            arguments = map_linked_list(eval_s_expression, arguments)
            
            for argument in flatten_linked_list(arguments):
                if type(argument) == int:
                    product *= argument
                else:
                    raise SchemeTypeError("Can't multiply something that isn't an integer.")
            return product

        return multiply_function

    elif symbol_string == '-':

        def subtract_function(arguments):
            if not arguments:
                raise SchemeTypeError("Subtract takes at least one argument")

            arguments = map_linked_list(eval_s_expression, arguments)
            head, tail = arguments

            if not tail:
                # only one argument, we just negate it
                return -1 * head
            else:
                total = head

                for argument in flatten_linked_list(tail):
                    total -= argument

                return total

        return subtract_function

    elif symbol_string == '=':

        def equality_function(arguments):
            if len_linked_list(arguments) < 2:
                raise SchemeTypeError("Equality test requires two arguments or more.")

            arguments = map_linked_list(eval_s_expression, arguments)

            head, tail = arguments

            for argument in flatten_linked_list(tail):
                if argument != head:
                    return False
            return True

        return equality_function
    
    elif symbol_string == 'define':

        def define_variable(arguments):
            if len_linked_list(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to `define`.")

            head, tail = arguments

            if isinstance(head, Atom):
                # variable assignment
                if head.type != 'SYMBOL':
                    raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % expression_type)

                if head.value in variables:
                    raise RedefinedVariable("Cannot define %s, as it has already been defined." % head.value)

                variables[head.value] = eval_s_expression(tail)

            else:
                # function definition
                function_name, function_parameters = head

                if function_name.type != "SYMBOL":
                    raise SchemeTypeError("Function names must be symbols, not a %s." % function_name.type)

                for parameter in flatten_linked_list(function_parameters):
                    if parameter.type != "SYMBOL":
                        raise SchemeTypeError("Function arguments must be symbols, not a %s." % parameter.type)

                function_body = tail

                def named_function(arguments):
                    if len_linked_list(arguments) != len_linked_list(function_parameters):
                        raise SchemeTypeError("%s takes %d arguments, %d given." % \
                                                  (function_name, len_linked_list(function_parameters), len_linked_list(arguments)))

                    # create function scope by saving old environment
                    global variables
                    global_variables = variables.copy()

                    # evaluate arguments
                    for (parameter_name, parameter_expression) in zip(flatten_linked_list(function_parameters),
                                                                      flatten_linked_list(arguments)):
                        variables[parameter_expression] = eval_s_expression(parameter_expression)

                    # evaluate the function block
                    result = eval_s_expression(function_body)

                    # restore old environment
                    variables = global_variables

                    return result

                # assign this function to this name
                variables[function_name] = named_function

        return define_variable

    elif symbol_string == 'set!':

        def set_variable(arguments):
            if len_linked_list(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to `set!`.")

            variable_name, variable_expression = arguments

            if variable_name.type != 'SYMBOL':
                raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % expression_type)

            if variable_name.value not in variables:
                raise UndefinedVariable("Can't assign to undefined variable %s." % atom_string)

            variables[variable_name.value] = eval_s_expression(variable_expression)

        return set_variable

    elif symbol_string == 'if':

        def if_function(arguments):
            if len_linked_list(arguments) not in [2,3]:
                raise SchemeTypeError("Need to pass either two or three arguments to `if`.")

            condition, tail = arguments
            condition = eval_s_expression(condition)

            then_expression, else_expression = tail
            
            # everything except an explicit false boolean is true
            if condition != False:
                return eval_s_expression(then_expression)
            else:
                if else_expression:
                    return eval_s_expression(else_expression)

        return if_function

    elif symbol_string == 'lambda':

        def make_lambda_function(arguments):
            if len_linked_list(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to `lambda`.")

            parameter_list, function_body = arguments

            if not isinstance(parameter_list, tuple):
                raise SchemeTypeError("The first argument to `lambda` must be list of variables.")

            for parameter in flatten_linked_list(parameter_list):
                if parameter.type != "SYMBOL":
                    raise SchemeTypeError("Paramaters of lambda functions must be symbols, not %s." % parameter.type)

            def lambda_function(_arguments):
                if len_linked_list(_arguments) != len_linked_list(parameter_list):
                    raise SchemeTypeError("Wrong number of arguments for this "
                                          "lambda function, was expecting %d, received %d" % (len_linked_list(parameter_list), len_linked_list(_arguments)))

                # save the global scope variables elsewhere so we can restore them
                global variables
                global_variables = variables.copy()

                for (parameter_name, parameter_expression) in zip(flatten_linked_list(parameter_list),
                                                                  flatten_linked_list(_arguments)):
                    variables[parameter_name.value] = eval_s_expression(parameter_expression)

                # now we have set up the correct scope, evaluate our function block
                result = eval_s_expression(function_body)

                # now restore the original environment
                variables = global_variables

                return result

            return lambda_function

        return make_lambda_function

    elif symbol_string == 'quote':

        def return_argument_unevaluated(arguments):
            if len_linked_list(arguments) != 1:
                raise SchemeTypeError("Quote takes exactly one argument, received %d" % len(arguments))

            head, tail = arguments
            return head

        return return_argument_unevaluated

    elif symbol_string in variables:

        return variables[symbol_string]

    else:

        raise UndefinedVariable('%s has not been defined (environment: %s).' % (symbol_string, variables))

def eval_boolean(boolean_string):
    if boolean_string == '#t':
        return True
    elif boolean_string == '#f':
        return False

def flatten_linked_list(linked_list):
    if not linked_list:
        return []

    head, tail = linked_list
    return [head] + flatten_linked_list(tail)

def map_linked_list(function, linked_list):
    if not linked_list:
        return None

    head, tail = linked_list
    return (function(head), map_linked_list(function, tail))

def len_linked_list(linked_list):
    if not linked_list:
        return 0

    head, tail = linked_list
    return 1 + len_linked_list(tail)
