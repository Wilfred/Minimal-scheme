class InterpreterException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Interpreter error: %s" % self.message

class CircularList(InterpreterException):
    pass

class UndefinedVariable(InterpreterException):
    pass

class RedefinedVariable(InterpreterException):
    pass

class SchemeTypeError(InterpreterException):
    # 'TypeError' is a built-in Python exception
    pass

class SchemeSyntaxError(InterpreterException):
    # SyntaxError is also a built-in Python exception
    pass

class SchemeArityError(InterpreterException):
    pass

class InvalidArgument(InterpreterException):
    pass

class SchemeStackOverflow(InterpreterException):
    def __init__(self):
        super().__init__("Stack overflown")

