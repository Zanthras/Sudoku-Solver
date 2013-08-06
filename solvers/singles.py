
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

def solve_singles(board, pboard):
    lone = look_for_lone_ptable_entries(pboard)
    if lone[0]:
        for value in lone[1]:
            msg = "possibility table at " + str(cflip(value[0])) + " has only a single entry which is the number " + str(value[1])
            support.update_gamestepslog("board", "add", value[0], value[1], msg, True)
            support.oo_update_actions(value[0], value[1], board, pboard)
        return True
    return False
solve_singles.name = "Singles"

def look_for_lone_ptable_entries(pboard):
    ''' finds suitable updates by looking for single length ptable entries '''
    # return format (boolean, [((y,x), num),((y,x), num)])
    boolean = False
    update_list = []
    for square in SQUARES:
        coords = get_coord_list(square, 2)
        for coord in coords:
            if len(pboard[coord[0]][coord[1]]) == 1:
                boolean = True
                update_list.append((coord, pboard[coord[0]][coord[1]][0]))
                # only return one to ensure steps dont get skipped
                return boolean, update_list
    return boolean, update_list
