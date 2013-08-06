
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
from grids import create_set_iterable


# more generic form of my related triplicate

# within a single line
#  add all 2 & 3 length coords to a list
#  if the length of the list is at least 3
#   #make unique sets of 3 length cells
#   create_set_iterable(3, number_of_lines)
#   for iterable check each coord and add all numbers to a set
#   if the length of the set is 3
#    i have 3 numbers in 3 cells perfect
#    for coord in full line
#     if coord not in set
#      for number in set
#       if number in line coord
#        remove number


def trim_cleanup(pboard, matched_coords, trimmed_list):
    first_entry = True
    display = []
    for coord in matched_coords:
        y, x = coord[0], coord[1]
        for num in pboard[y][x]:
            display.append((coord, num, "set1"))
    for entry in trimmed_list:
        if first_entry:
            first_entry = False
            GAMESTEPS[0] += 1
            display.append((entry[0], entry[1], "remove"))
        else:
            display = [(entry[0], entry[1], "remove")]
        msg = "Removed " + str(entry[1]) + " because its sees a naked triplicate"
        support.update_gamestepslog('pboard', 'remove', entry[0], entry[1], msg, False, display)


def line_trim(pboard, line_coords, matched_coords, trimmed, poss_set):
    for line_coord in line_coords:
        if line_coord not in matched_coords:
            for trip_num in poss_set:
                if trip_num in pboard[line_coord[0]][line_coord[1]]:
                    trimmed.append((line_coord, trip_num))
                    pboard[line_coord[0]][line_coord[1]].remove(trip_num)

def related_trips(board, pboard):
    any_trim = False
    for x_type in range(3):
        for line in LINES[x_type]:
            proper_len_cells = []
            full_line_coords = get_coord_list(line, x_type)
            for coord in full_line_coords:
                y, x = coord[0], coord[1]
                if 2 <= len(pboard[y][x]) <= 3:
                    proper_len_cells.append(coord)
            if len(proper_len_cells) >= 3:
                unique_sets = create_set_iterable(3, len(proper_len_cells))
                for unique_set in unique_sets:
                    poss_set = set()
                    matched_coords = []
                    for num in unique_set:
                        y, x = proper_len_cells[num][0], proper_len_cells[num][1]
                        for poss in pboard[y][x]:
                            poss_set.add(poss)
                            matched_coords.append((y, x))
                    # I found a naked triplicate
                    if len(poss_set) == 3:
                        trimmed = []
                        #cleanup the current line
                        line_trim(pboard, full_line_coords, matched_coords, trimmed, poss_set)
                        #check if all matched coords are in the same square
                        if x_type == 0 or x_type == 1:
                            square_coords = get_coord_list(matched_coords[0], 2)
                            is_same_square = True
                            for coord in matched_coords:
                                if coord not in square_coords:
                                    is_same_square = False
                            #cleanup the rest of the square
                            if is_same_square:
                                line_trim(pboard, square_coords, matched_coords, trimmed, poss_set)
                        if trimmed:
                            trim_cleanup(pboard, matched_coords, trimmed)
                            return True
    return any_trim
related_trips.name = "Naked Triplicates"

