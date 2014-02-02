def compile_scm():
    template = """	.text
	.globl	entry_point
entry_point:
	movl	$26, %eax
	ret
    """
    return template


if __name__ == '__main__':
    with open('scheme.s', 'w') as f:
        f.write(compile_scm())
