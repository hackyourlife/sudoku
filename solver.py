#!/bin/python
# vim:set ts=8 sts=8 sw=8 tw=80 noet:

import sys

NUMBERS = range(1, 10)

def read(filename):
	def parse(x):
		tokens = [ x[i] for i in range(len(x)) ]
		return [ int(i) if i != "-" else None \
				for i in tokens ]

	with open(filename) as f:
		return [ parse(x.strip()) for x in f ]

def get_3x3(x, y, sudoku):
	x *= 3
	y *= 3
	rows = sudoku[y:y + 3]
	z = [ r[x:x + 3] for r in rows ]
	return z

def get_possible(x, y, sudoku):
	r = sudoku[y]
	c = [ z[x] for z in sudoku ]
	f = get_3x3(int(x / 3), int(y / 3), sudoku)
	s = []
	for row in f:
		for column in row:
			s += [ column ]
	free = [ n for n in NUMBERS \
			if not n in r \
			and not n in c \
			and not n in s ]
	return free

def validate(sudoku):
	global NUMBERS
	def validate_3x3(x, y, sudoku):
		r = get_3x3(x, y, sudoku)
		z = []
		for row in r:
			for i in row:
				if i is None:
					continue
				if i in z:
					return False
				z += [ i ]
		return True
	r = [ [] for i in range(len(sudoku[0])) ]
	for row in sudoku:
		z = []
		for i in range(len(row)):
			x = row[i]
			if x is None:
				continue
			if not x in NUMBERS:
				return False
			if x in z:
				return False
			z += [ x ]
			if x in r[i]:
				return False
			r[i] += [ x ]
	for y in range(len(sudoku)):
		for x in range(len(sudoku[y])):
			if not validate_3x3(x, y, sudoku):
				return False
	return True

def solve(sudoku):
	found = False
	for y in range(len(sudoku)):
		for x in range(len(sudoku[y])):
			if not sudoku[y][x] is None:
				continue
			found = True
			possible = get_possible(x, y, sudoku)
			if len(possible) == 0:
				return None
			for n in possible:
				sudoku[y][x] = n
				z = solve(sudoku)
				if not z is None:
					return z
			sudoku[y][x] = None
			return None
	if not found:
		return sudoku
	return None

def show(sudoku):
	for line in sudoku:
		print(" ".join([ str(x) if not x is None \
				else "-" for x in line ]))

if __name__ == "__main__":
	if len(sys.argv) != 2:
		sys.stderr.write("Usage: %s sudoku-file\n" \
				% sys.argv[0])
		sys.exit(1)
	sudoku = read(sys.argv[1])
	if not validate(sudoku):
		print("Sudoku contains errors")
		sys.exit(2)
	solved = solve(sudoku)
	if solved is None:
		print("no solution")
	else:
		show(solved)
