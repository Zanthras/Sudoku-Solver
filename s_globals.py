
'''
Copyright 2013 Joel Whitcomb

This file is part of Sudoku Solver.

    Sudoku Solver is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Sudoku Solver is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Sudoku Solver.  If not, see <http://www.gnu.org/licenses/>
'''

list1 = [0, 1, 2,]
list2 = [3, 4, 5,]
list3 = [6, 7, 8,]
list4 = [0, 3, 6,]
list5 = [1, 4, 7,]
list6 = [2, 5, 8,]
list7 = [1, 2, 3,]
list8 = [4, 5, 6,]
list9 = [7, 8, 9,]

trim_type_lookup = {0:"row", 1:"column", 2:"square",}



NUMS_COUNT = [0,0,0,0,0,0,0,0,0,0]
NUMBERS = range(1,10)
ROWS = range(9)
COLUMNS = range(9)
SQUARES = range(9)
ROWS_SUM = [0,0,0,0,0,0,0,0,0]
COLS_SUM = [0,0,0,0,0,0,0,0,0]
SQUS_SUM = [0,0,0,0,0,0,0,0,0]
SUMS = [ROWS_SUM, COLS_SUM, SQUS_SUM]
LINES = [ROWS, COLUMNS, SQUARES]


blank_board = [[0,0,0,0,0,0,0,0,0,] for i in range(9)]
blank_pboard = [[[] for i in range(9)] for i in range(9)]


GAMESTEPSLOG = []
GAMESTEPS = [0]

STEP_COLOR_INFO = []
WEB_GAMELOG = ['']


# sets mode solve
SOLVE = []

# OO solve it stuff
STEPSREQUIRED = [0]

init_board = [[0,0,0,0,0,0,0,0,0,] for i in range(9)]

# record all uses of my solvers
SOLVER_STATS = {}

# timekeeper

SOLVER_TIMES = {}
