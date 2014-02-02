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


if __name__ == '__main__':
    # todo: lex and parse
    program = 34
    
    with open('scheme.s', 'w') as f:
        f.write(compile_scm(program))
