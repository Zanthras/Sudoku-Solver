
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

# basic version 
# find every 3 possibility cell
# check if each key can see at least 2 corners (key is a 2 length cell)
#   check each unique corner combination
#    check if there are only 3 possibilities total
#     find the common possibility
#      get the seen coords of the two corners
#      find the intersection of all seen coords (remove the key and corners)
#      remove the common possibility from all the intersected coords
 
 
# --- more advanced version---
 
# for every cell that has between 2 and 4 possibilities
# find all cells(corners) that it can see that has between 2 and 4 possibilities
#   for all unique sets of corners
#    check if there are only 4 possibilities
#     build a dictionary of possibilities (key is possibility, val is list of coords)
#      check n-1 coords for each key to see if it can see every other coord
#       if one cant
#        find the intersection of seen coords of just that possibility
#         remove the possibility from those intersected coords


import support
from s_info import *
from s_globals import *

from grids import create_set_iterable


def find_keys(pboard):
    keys = []
    for y in range(9):
        for x in range(9):
            if len(pboard[y][x]) == 3:
               keys.append((y, x))
    if len(keys) > 0:
        return keys
    else:
        return False

def seen_coords(pboard, coord, include_self=False):
    all_coords = set()
    for x_type in range(3):
        coords = get_coord_list(coord, x_type)
        for c in coords:
            all_coords.add(c)
    if not include_self:
        all_coords.remove(coord)
    return all_coords

def find_corners(pboard, key):
    seen_coords_list = seen_coords(pboard, key)
    potential_corners = []
    for coord in seen_coords_list:
        y, x = coord[0], coord[1]
        if len(pboard[y][x]) == 2:
            potential_corners.append(coord)
    if len(potential_corners) >= 2:
        return potential_corners
    else:
        return False

def validate_corners(pboard, key, corners):
    possibilities = set()
    for num in pboard[key[0]][key[1]]:
        possibilities.add(num)
    for corner in corners:
        for num in pboard[corner[0]][corner[1]]:
            possibilities.add(num)
    if len(possibilities) == 3:
        # log(0, possibilities)
        # log(0, pboard[key[0]][key[1]])
        # log(0, pboard[corners[0][0]][corners[0][1]])
        # log(0, pboard[corners[1][0]][corners[1][1]])
        shared_num = list(possibilities)
        for num in possibilities:
            for corner in corners:
                if num not in pboard[corner[0]][corner[1]]:
                    #log(0, "removing" + str(num))
                    try:
                        shared_num.remove(num)
                    except ValueError:
                        # [1,2,3], [1,2], [1,2] is not to be acted on!
                        return False
        return shared_num, possibilities
    return False

def trim_cleanup(pboard, key, corners, match_nums, trimmed_list, msg):
    first_entry = True
    display = []
    for num in match_nums:
        display.append((key, num, "set1"))
    for corner in corners:
        y, x = corner[0], corner[1]
        for num in pboard[y][x]:
            if num in match_nums:
                display.append((corner, num, "set1"))
    for entry in trimmed_list:
        if first_entry:
            first_entry = False
            GAMESTEPS[0] += 1
            display.append((entry[0], entry[1], "remove"))
        else:
            display = [(entry[0], entry[1], "remove")]
        display_msg = "Removed " + str(entry[1]) + msg
        support.update_gamestepslog('pboard', 'remove', entry[0], entry[1], display_msg, False, display)


def hinged_match(board, pboard):
    keys = find_keys(pboard)
    if keys:
        for key in keys:
            corners = find_corners(pboard, key)
            if corners:
                unique_sets = create_set_iterable(2, len(corners))
                for unique_set in unique_sets:
                    real_corners = []
                    for num in unique_set:
                        real_corners.append(corners[num])
                    shared_nums = validate_corners(pboard, key, real_corners)
                    if shared_nums:
                        corner1seen = seen_coords(pboard, real_corners[0])
                        corner2seen = seen_coords(pboard, real_corners[1])
                        keyseen = seen_coords(pboard, key)
                        allseen = corner1seen & corner2seen & keyseen
                        trimmed = []
                        for shared_num in shared_nums[0]:
                            for coord in allseen:
                                if shared_num in pboard[coord[0]][coord[1]]:
                                    pboard[coord[0]][coord[1]].remove(shared_num)
                                    trimmed.append((coord, shared_num))
                                    # log(0, key)
                                    # log(0, real_corners)
                                    # log(0, coord)
                                    #return
                        if trimmed:
                            msg = " because its seen by every member of the hinged match"
                            trim_cleanup(pboard, key, real_corners, shared_nums[1], trimmed, msg)
                            return True
    return False
hinged_match.name = "Hinged Match"
