'''
Created on Jun 17, 2014

@author: Daniel Norman
Copyright Daniel Norman 2014
'''
from tile import Tile
from number import Number
from nonogram_solver import NonogramSolver
import time




solver = NonogramSolver()
functions = [
             solver.check_overlap,
             solver.check_overlap_without_owners,
             solver.check_empty_group,
             solver.check_filled_between,
             solver.check_owners,
             solver.check_sides,
             solver.check_filled_constrained,
             ]

numbs = [
         [2]
         ,[1,1]
         ,[1,1]
         ,[1,1,3]
         ,[1,1,5]
         
         ,[1,1,1,1]
         ,[7,3,1]
         ,[1,1,1,5]
         ,[6,6]
         ,[1,1]
         
         ,[5]
         ,[2,2]
         ,[2,2]
         ,[2,2]
         ,[5]
         
         
         ,[2]
         ,[1,1]
         ,[1,1]
         ,[1,1,3]
         ,[1,1,5]
         
         ,[1,1,1,1]
         ,[11,1]
         ,[1,5]
         ,[14]
         ,[1,1]
         
         ,[5]
         ,[2,2]
         ,[2,2]
         ,[2,2]
         ,[4]
         ]

numbers = [[Number(numbs[j][i]) for i in range(len(numbs[j]))] for j in range(len(numbs))]



grid = [[Tile() for _ in range(len(numbs) / 2)] for _ in range(len(numbs) / 2)]


start = time.clock()
solver.solve_grid(grid, numbers, functions, 50)
end = time.clock()
print 'Solving took %sms.' % (round((end - start) * 1000, 1))

solver.print_grid(grid, 'X', ' ', '_')