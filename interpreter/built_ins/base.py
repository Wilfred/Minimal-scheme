built_ins = {}

# a decorator for giving a name to built-in
def name_function(function_name):
    def name_function_decorator(function):
        built_ins[function_name] = function

        # we return the function too, so we can use multiple decorators
        return function

    return name_function_decorator


