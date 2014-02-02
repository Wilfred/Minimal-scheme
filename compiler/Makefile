all: main

scheme.s: compiler.py
	python2 compiler.py

main: runtime.c scheme.s
	gcc -Wall runtime.c scheme.s -o main
