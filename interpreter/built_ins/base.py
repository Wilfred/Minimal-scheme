built_ins = {}

# a decorator for giving a name to built-in
def define_built_in(function_name):
    def define_built_in_decorator(function):
        built_ins[function_name] = function

        # we return the function too, so we can use multiple decorators
        return function

    return define_built_in_decorator


