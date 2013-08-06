
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

def line_pointing(board, pboard):
    for trim_type in range(2):
        if trim_ptable_for_num_in_line(pboard, trim_type):
            return True
    return False
line_pointing.name = "Line Pointing"

def trim_ptable_for_num_in_line(pboard, trim_type):
    ''' Looks for a number appearing only in a line in a single square '''
    trim_type_lookup = { 0:"row", 1:"column"}
    any_trim = False
    for square in SQUARES:
        coords = get_coord_list(square, 2)
        if trim_type == 0:
            # take first (upper left cell) coord and iterate off Y
            iterate_base = coords[0][0]
        if trim_type == 1:
            # take first (upper left cell) coord and iterate off X
            iterate_base = coords[0][1]
        # look through all three rows/columns, no more no less
        for i in range(3):
            # iterate_base is the current row/column number
            iterate_now = i + iterate_base
            current_set = set()
            rest_of_line_set = set()
            rest_of_square_set = set()
            current_line = []
            rest_of_line = []
            rest_of_square = []
            for coord in coords:
                if trim_type == 0:
                    comparison = coord[0]
                if trim_type == 1:
                    comparison = coord[1]
                if comparison == iterate_now:
                    # can update whole line except if in my square... ie current_line
                    current_line.append(coord)
                    for element in pboard[coord[0]][coord[1]]:
                        current_set.add(element)
                else:
                    rest_of_square.append(coord)
                    for element in pboard[coord[0]][coord[1]]:
                        rest_of_square_set.add(element)
            # check for a number existing only in the currentset
            uniqueset = current_set - rest_of_square_set
            
            # get row/column coord list
            line_list = get_coord_list(current_line[0], trim_type)
            for coord in line_list:
                if coord not in current_line:
                    rest_of_line.append(coord)
                    for element in pboard[coord[0]][coord[1]]:
                        rest_of_line_set.add(element)
            if len(uniqueset) >= 1:
                for u_num in uniqueset:
                    #log(0,uniqueset)
                    #log(0, str(square) + " square")
                    # clear the number from the rest of the line
                    uniquenum = u_num
                    # clean the rest of the line
                    first_trim = True
                    for coord in line_list:
                        if coord not in current_line:
                            if uniquenum in pboard[coord[0]][coord[1]]:
                                msg = "trimmed " + str(uniquenum) + " because it has to be in " + trim_type_lookup[trim_type] + " " + str(iterate_now + 1) + " in square " + str(square + 1)
                                display = [(coord, uniquenum, 'remove'), ]
                                for entry in current_line:
                                    display.append((entry, uniquenum, 'set1'))
                                if first_trim:
                                    any_trim = True
                                    support.update_gamestepslog('pboard', 'remove', coord, uniquenum, msg, True, display)
                                    first_trim = False
                                else:
                                    support.update_gamestepslog('pboard', 'remove', coord, uniquenum, msg, False, display)
                                pboard[coord[0]][coord[1]].remove(uniquenum)
                    # only update 1 number
                    if any_trim:
                        return True
            # checking for requirement to "only" be in a certain row/column
            for i in range(len(current_set)):
                numtoeval = current_set.pop()
                if numtoeval not in rest_of_line_set:
                    if numtoeval in rest_of_square_set:
                        first_trim = True
                        for coord in rest_of_square:
                            if numtoeval in pboard[coord[0]][coord[1]]:
                                msg = "trimmed " + str(numtoeval) + " because in square " + str(square + 1) + " the number can only be in " + trim_type_lookup[trim_type] + " " + str(iterate_now + 1) 
                                display = [(coord, numtoeval, 'remove')]
                                for entry in current_line:
                                    display.append((entry, numtoeval, 'set1'))
                                if first_trim:
                                    any_trim = True
                                    support.update_gamestepslog('pboard', 'remove', coord, numtoeval, msg, True, display)
                                    first_trim = False
                                else:
                                    support.update_gamestepslog('pboard', 'remove', coord, numtoeval, msg, False, display)
                                pboard[coord[0]][coord[1]].remove(numtoeval)
    return any_trim
