from collections import Sequence

class Atom(object):
    """An abstract class for every base type in Scheme."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "<Atom: %s (%s)>" % (str(self.value), self.__class__.__name__)

    def __eq__(self, other):
        if isinstance(other, self.__class__) and other.value == self.value:
            return True

        return False

    def get_python_equivalent(self):
        return self.value


"""Atom classes. Although most Scheme data types map neatly to Python
equivalents, there are some exceptions (such as symbols and exact
fractions). Therefore we wrap all atoms in a class so we can treat
them uniformly.

"""
class Symbol(Atom):
    def get_external_representation(self):
        return self.value

class Number(Atom):
    def __eq__(self, other):
        # we allow different types to be equal only for numbers
        if isinstance(other, Number) and self.value == other.value:
            return True

        return False

    def get_external_representation(self):
        return str(self.value)


class Integer(Number):
    pass

class FloatingPoint(Number):
    pass

class Boolean(Atom):
    def get_external_representation(self):
        if self.value:
            return "#t"
        else:
            return "#f"


class Character(Atom):
    def get_external_representation(self):
        return "#\%s" % self.value


class String(Atom):
    def get_external_representation(self):
        return "%r" % self.value


class Cons(Sequence):
    @staticmethod
    def from_list(python_list):
        if not python_list:
            return Nil()
        else:
            head = python_list[0]
            tail = Cons.from_list(python_list[1:])
            return Cons(head, tail)

    def __init__(self, head, tail=None):
        self.head = head

        if tail:
            self.tail = tail
        else:
            self.tail = Nil()
            

    def __len__(self):
        return 1 + self.tail.__len__()

    def __getitem__(self, index):
        if index == 0:
            return self.head
        else:
            return self.tail.__getitem__(index - 1)

    def __setitem__(self, index, value):
        if index == 0:
            self.head = value
        else:
            return self.tail.__setitem__(index - 1, value)

    def __repr__(self):
        return "<Cons: %s>" % str(self.get_python_equivalent())

    def __bool__(self):
        # a cons represents is a non-empty list, which we treat as true
        return True

    def get_python_equivalent(self):
        if hasattr(self.head, "get_python_equivalent"):
            python_list = [self.head.get_python_equivalent()]
        else:
            python_list = [self.head]

        if isinstance(self.tail, Atom):
            # an improper list has an atom as a tail rather than a list
            return python_list + ['.', self.tail.get_python_equivalent()]
        else:
            # normal list
            return python_list + self.tail.get_python_equivalent()

    def get_external_representation(self):
        items = [item.get_external_representation() for item in self]
        return "(%s)" % ' '.join(items)


class Nil(Sequence):
    # the empty list for our linked list structure
    def __len__(self):
        return 0

    def __getitem__(self, index):
        raise IndexError

    def __setitem__(self, index, value):
        raise IndexError

    def __repr__(self):
        return "<Nil>"

    def __bool__(self):
        return False

    def __eq__(self, other):
        # a Nil is always equal to a Nil
        if isinstance(other, Nil):
            return True
        return False

    def get_python_equivalent(self):
        return []

    def get_external_representation(self):
        return "()"

class Vector(Sequence):
    def __init__(self, length):
        self.value = []
        for index in range(length):
            self.value.append(Nil())

    def __getitem__(self, index):
        return self.value[index]

    def __len__(self):
        return len(self.value)

    def __eq__(self, other):
        if isinstance(other, Vector) and self.value == other.value:
            return True

        return False

    def get_external_representation(self):
        item_reprs = [item.get_external_representation()
                      for item in self.value]
        return "#(%s)" % (" ".join(item_reprs))


"""Function classes. These are currently only used in order to add an
external representation.

"""

class Function(object):
    def __init__(self, func, name):
        self.function = func
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class BuiltInFunction(Function):
    def get_external_representation(self):
        return "#<built-in function %s>" % self.name


class PrimitiveFunction(Function):
    def get_external_representation(self):
        return "#<primitive function %s>" % self.name


class UserFunction(Function):
    def get_external_representation(self):
        return "#<user function %s>" % self.name
    

class LambdaFunction(Function):
    def __init__(self, func):
        self.function = func

    def get_external_representation(self):
        return "#<anonymous function>"
