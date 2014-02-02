from subprocess import check_output
from unittest import main, TestCase

from compiler import create_binary

class LiteralIntegerTest(TestCase):
    def assertEvaluatesRepr(self, program, result_repr):
        """Assert that the given program, when compiled and executed, writes
        result_repr to stdout.

        """
        create_binary(program)
        self.assertEqual(check_output(['./main']).strip(), result_repr)
    
    def test_42(self):
        self.assertEvaluatesRepr(42, "42")


if __name__ == '__main__':
    main()
