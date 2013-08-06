
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

import support
from s_info import *
from s_globals import *



def solve_single_possible(board, pboard):
    placed = False
    type_x_lookup = {0:"row", 1:"column", 2:"square"}
    possible = look_for_single_poss_numbers(pboard)
    if possible[0]:
        for value in possible[1]:
            msg = "the number " + str(value[1]) + " showed up only once in the possibility table for its " + str(type_x_lookup[value[2]])
            support.update_gamestepslog(b_type="board", func="add", coord=value[0], num=value[1], msg=msg, step_up=True)
            support.oo_update_actions(value[0], value[1], board, pboard)
        placed = True
    return placed
solve_single_possible.name = "Single Possible"



def look_for_single_poss_numbers(pboard):
    ''' finds suitable updates by looking for ptable numbers showing up once per row|column|square '''
    # return format (boolean, [((y,x), num, type_x),((y,x), num, type_x)])
    boolean = False
    update_list = []
    for type_x in range(3):
        for value in LINES[type_x]:
            values = []
            coords = get_coord_list(value, type_x)
            # make list of all possble numbers
            for coord in coords:
                values.extend(pboard[coord[0]][coord[1]])
            # if number shows up once its golden
            for number in NUMBERS:
                if values.count(number) == 1:
                    boolean = True
                    # figure out which box it is
                    for i in range(len(coords)):
                        if number in pboard[coords[i][0]][coords[i][1]]:
                            update_list.append((coords[i], number, type_x))
                            # only return one to ensure steps dont get skipped
                            return boolean, update_list
    return boolean, update_list
