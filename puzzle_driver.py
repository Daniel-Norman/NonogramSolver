'''
Created on Jun 17, 2014

@author: Daniel Norman
Copyright Daniel Norman 2014
'''
from tile import Tile
from number import Number
from nonogram_solver import NonogramSolver


numbs1 = [Number(3), Number(4)]

row = [Tile() for x in range(15)]
row[1].set_empty()
row[13].set_empty()
row[12].set_filled(numbs1[1])
row[3].set_filled(numbs1[0])

solver = NonogramSolver()
    


solver.print_row(row, numbs1)

functions = [solver.check_overlap, solver.check_filled_between, solver.check_filled_constrained, solver.check_empty_between]
for func in functions:
    func(row, numbs1)
    solver.check_sides(row, numbs1)


solver.print_row(row, numbs1)

