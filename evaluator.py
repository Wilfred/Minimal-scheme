from parser import parser


class InterpreterException(Exception):
    def __init__(self, message):
        self.message = message

class UndefinedVariable(InterpreterException):
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
    expression_type, expression = s_expression

    if expression_type == 'LIST':
        return eval_list(expression)
    elif expression_type == 'ATOM':
        return eval_atom(expression)

def eval_list(lst): # list is a reserved word
    # since every list is a linked list, we flatten the tail:
    # i.e. (+ 1 2) is stored as (+, (1, (2, None)))

    head, tail = lst

    arguments = []
    while tail:
        arguments.append(tail[0])
        tail = tail[1]

    # find the function we are calling
    function = eval_s_expression(head)

    # call it (we require the function to decide whether or not to
    # evalue the arguments)
    return function(arguments)


def eval_atom(atom):
    atom_type, atom_string = atom

    if atom_type == 'NUMBER':
        return eval_number(atom_string)
    elif atom_type == 'SYMBOL':
        return eval_symbol(atom_string)
    elif atom_type == 'BOOLEAN':
        return eval_boolean(atom_string)

def eval_number(number_string):
    return int(number_string)

def eval_symbol(symbol_string):
    if symbol_string == '+':

        def add_function(arguments):
            total = 0
            for argument in arguments:
                argument = eval_s_expression(argument)

                if type(argument) == int:
                    total += argument
                else:
                    raise SchemeTypeError("Can't add something that isn't an integer.")
            return total

        return add_function

    elif symbol_string == '*':

        def multiply_function(arguments):
            product = 1

            for argument in arguments:
                argument = eval_s_expression(argument)

                if type(argument) == int:
                    product *= argument
                else:
                    raise SchemeTypeError("Can't multiply something that isn't an integer.")
            return product

        return multiply_function

    elif symbol_string == '-':

        def subtract_function(arguments):
            if len(arguments) == 0:
                raise SchemeTypeError("Subtract takes at least one argument")
            elif len(arguments) == 1:
                return -1 * eval_s_expression(arguments[0])
            else:
                total = eval_s_expression(arguments[0])

                for argument in arguments[1:]:
                    total -= eval_s_expression(argument)

                return total

        return subtract_function

    elif symbol_string == '=':

        def equality_function(arguments):
            if len(arguments) < 2:
                raise SchemeTypeError("Equality test requires two arguments or more.")

            first_operand = eval_s_expression(arguments[0])

            for argument in arguments[1:]:
                if eval_s_expression(argument) != first_operand:
                    return False
            return True

        return equality_function
    
    elif symbol_string == 'define':

        def save_variable(arguments):
            if len(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to `define`.")

            expression_type, expression = arguments[0]

            if expression_type != 'ATOM':
                raise SchemeTypeError("Can't assign to %s, must an atom." % expression_type)

            atom_type, atom_string = expression

            if atom_type != 'SYMBOL':
                raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % expression_type)

            variables[atom_string] = eval_s_expression(arguments[1])

        return save_variable

    elif symbol_string == 'if':

        def if_function(arguments):
            if len(arguments) != 3:
                raise SchemeTypeError("Need to pass exactly three arguments to `if`.")

            condition = eval_s_expression(arguments[0])

            # everything except an explicit false boolean is true
            if condition == False:
                return eval_s_expression(arguments[2])
            else:
                return eval_s_expression(arguments[1])

        return if_function

    elif symbol_string == 'lambda':

        def make_lambda_function(arguments):
            if len(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to `lambda`.")

            expression_type, expression = arguments[0]

            if expression_type != 'LIST':
                raise SchemeTypeError("The first argument to `lambda` must be list of variables.")

            head, tail = expression
            variable_names = []
            while True:
                variable_expression_type, variable_expression = head

                if variable_expression_type != 'ATOM':
                    raise SchemeTypeError("Can only assign to atoms, not %s in lambda expressions." % variable_expression_type)

                atom_type, atom_string = variable_expression

                if atom_type != 'SYMBOL':
                    raise SchemeTypeError("Can only assign to symbols, not %s." % atom_type)

                # it checks out as a valid variable name, so save it
                variable_names.append(atom_string)

                if tail is None:
                    break

                head, tail = tail

            def lambda_function(_arguments):
                if len(_arguments) != len(variable_names):
                    raise SchemeTypeError("Wrong number of arguments for this "
                                          "lambda function, was expecting %d, received %d" % (len(variable_names), len(_arguments)))

                # save the global scope variables elsewhere so we can restore them
                global variables
                global_variables = variables.copy()

                for (variable_name, variable_expression) in zip(variable_names, _arguments):
                    variables[variable_name] = eval_s_expression(variable_expression)

                # now we have set up the correct scope, evaluate our function block
                result = eval_s_expression(arguments[1]) 

                # now restore the original environment
                variables = global_variables

                return result


            return lambda_function

        return make_lambda_function

    elif symbol_string == 'quote':

        def return_argument_unevaluated(arguments):
            if len(arguments) != 1:
                raise SchemeTypeError("Quote takes exactly one argument, received %d" % len(arguments))

            return arguments[0]

        return return_argument_unevaluated

    elif symbol_string in variables:

        return variables[symbol_string]

    else:

        raise UndefinedVariable('%s has not been defined.' % symbol_string)

def eval_boolean(boolean_string):
    if boolean_string == '#t':
        return True
    elif boolean_string == '#f':
        return False
