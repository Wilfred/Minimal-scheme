import os


def compile_literal(value):
    return "movl	$%s, %%eax" % value


def compile_scm(code):
    asm = ""
    if isinstance(code, int):
        asm += compile_literal(code)
    
    template = """	.text
	.globl	entry_point
entry_point:
	%s
	ret
    """ % (asm,)

    return template

    with open('scheme.s', 'w') as f:
        f.write(template)


def create_binary(program):
    """Given text of a scheme program, write assembly and link it into an
    executable.

    """
    # todo: lex and parse
    
    with open('scheme.s', 'w') as f:
        f.write(compile_scm(program))

    os.system('gcc runtime.c scheme.s -o main')

    
if __name__ == '__main__':
    program = 34
    create_binary(program)
