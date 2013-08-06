'''Fairly smart sudoku solver'''
# coding=utf-8

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

import time
import sys

import solvers
import publish
import support

from s_globals import *
from s_info import *
from s_tests import *


#---------------------------main function---------------------------



def try_oo_solver(board, pboard, steps):
    while True:
        current_step = int(GAMESTEPS[0])
        # board complete check
        if oo_is_done(board, pboard, steps):
            break
        # all solve functions *must* have the same 2 inputs, and must output a boolean indicating work done
        for solver in SOLVER_LIST:
            starttime = time.time()
            progress = solver(board, pboard)
            stoptime = time.time() - starttime
            if solver.name not in SOLVER_TIMES:
                SOLVER_TIMES[solver.name] = stoptime
            else:
                SOLVER_TIMES[solver.name] += stoptime
            if progress:
                updates(solver)
                break
        # If there is progress start loop again
        if GAMESTEPS[0] > current_step:
            continue
        # Couldnt solve, stopping...
        log(1, "Couldnt solve the board.")
        oo_is_done(board, pboard, steps, True)
        break

def updates(solver):
    msg = "Used %s to make progress" % solver.name
    #log(0, msg)
    if solver.name not in SOLVER_STATS:
        SOLVER_STATS[solver.name] = 1
    else:
        SOLVER_STATS[solver.name] += 1

def oo_solveit(steps, board):
    global pboard
    pboard = unshared_copy(blank_pboard)
    # copy the board into the init_board
    for y in range(9):
        for x in range(9):
            init_board[y][x] = board[y][x]
    generate_possibility_table(board, pboard)
    try_oo_solver(board, pboard, steps)
    return


def main(steps, board, oo=False):
    log(1, "Solve Started")
    boardid = 'board id: '
    for r in board:
        for c in r:
            boardid += str(c)
    log(1, boardid)
    start = time.time()
    if not oo:
        log(1, "Solve Started")
        solveit(steps, board)
    else:
        log(1, "Object Oriented Solve Started")
        oo_solveit(steps, board)
    publish.publish_table(steps)
    stop = time.time() - start
    log(1, "Solve Complete taking %s seconds" % str(stop) )
    boardid = 'board id: '
    for r in board:
        for c in r:
            boardid += str(c)
    log(1, boardid)
    for entry in GAMESTEPSLOG:
        #log(0, entry)
        pass
    totaltime = 0.0
    for solver in SOLVER_TIMES:
        totaltime += SOLVER_TIMES[solver]
        log(0, solver + " " +  str(SOLVER_TIMES[solver]))
    log(0, "Total " + str(totaltime))


def generate_possibility_table(board, pboard):
    ''' using the same method as basic solver but instead put every valid response in the ptable '''
    for number in NUMBERS: # loop through every number to try and place
        for square in SQUARES: #loop through every square for every number
            small_square_list = get_small_square_list(square, board)
            if number not in small_square_list:
                for i in range(9):
                    if small_square_list[i] == 0:
                        coordsy, coordsx = lookup_array_coord(square, i)
                        if number not in get_row_list(coordsy, board):
                            if number not in get_column_list(coordsx, board):
                                pboard[coordsy][coordsx].append(number)
                                coord = (coordsy, coordsx)
                                update_gamestepslog('pboard', "add", coord, number, "pboard init", False)

#---------------------------Solve Order---------------------------


SOLVER_LIST = [

solvers.solve_singles,
solvers.solve_single_possible,
solvers.naked_entries,
solvers.hidden_matches,
solvers.related_trips,
solvers.line_pointing,
solvers.locked_pairs,
solvers.simple_chain,
solvers.complex_chain,
solvers.corner_intersect,
solvers.hinged_match,
solvers.trip_grid,
solvers.quad_grid,
solvers.medusa_chain,
solvers.hinged_quad,

]
