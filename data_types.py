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
    pass

class Number(Atom):
    pass

class Integer(Number):
    pass

class FloatingPoint(Number):
    pass

class Boolean(Atom):
    pass

class Character(Atom):
    pass

class String(Atom):
    pass

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
