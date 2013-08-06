
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

from hinged import seen_coords
from grids import create_set_iterable

def find_keys(pboard, max_length):
    keylist = []
    for x in range(9):
        for y in range(9):
            if 2 <= len(pboard[y][x]) <= max_length:
                keylist.append((y,x))
    return keylist

def find_non_restricted_nums(pboard, possibilities, corners):
    ''' returns a list of numbers that cant see every other number in the corner set '''
    number_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]} 
    non_restricted = set()
    # create a listing of where every number appears in my set
    for coord in corners:
        for poss in pboard[coord[0]][coord[1]]:
            number_dict[poss].append(coord)
    #log(0, number_dict)
    #log(0, possibilities)
    for poss_num in possibilities:
        #log(0, "checking the possibility " + str(poss_num))
        for i in range(len(number_dict[poss_num]) - 2):
        #for coord in number_dict[poss_num]:
            coord = number_dict[poss_num][i]
            #log(0, "building coords seen by " + str(coord))
            seen = seen_coords(pboard, coord, True)
            for compare_coord in number_dict[poss_num]:
                #log(0, "checking " + str(compare_coord))
                if compare_coord not in seen:
                    non_restricted.add(poss_num)
                    if len(non_restricted) > 1:
                        return False
    #log(0, non_restricted)
    if len(non_restricted) == 1:
        result = []
        for num in non_restricted:
            result.append((num, number_dict[num]))
        return result
    else:
        return False

def find_common_coord(pboard, not_restricted_nums):
    ''' Returns a listing of coords that can be seen by every possibility in the set that have the number in them '''
    results = []
    #log(0, not_restricted_nums)
    for candidate_info in not_restricted_nums:
        firstcoord = True
        common_coords = set()
        for coord in candidate_info[1]:
            if firstcoord:
                firstcoord = False
                common_coords = seen_coords(pboard, coord)
            else:
                corner_seen_coords = seen_coords(pboard, coord)
                common_coords = corner_seen_coords & common_coords
        num_seen_in_coord = []
        for coord in common_coords:
            if candidate_info[0] in pboard[coord[0]][coord[1]]:
                num_seen_in_coord.append(coord)
        if len(num_seen_in_coord) > 0:
            results.append((candidate_info[0], num_seen_in_coord))
    return results

def trim_and_report(pboard, things_to_trim, real_corners, x_length, key):
    x_length_lookup = {3:"triplicate", 4:"quadruplicate"}
    #log(0, things_to_trim)
    display = []
    #log(0, real_corners)
    for coord in real_corners:
        if coord != key:
            for poss in pboard[coord[0]][coord[1]]:
                display.append((coord, poss, "set1"))
    for poss in pboard[key[0]][key[1]]:
        display.append((key, poss, "set2"))
    first_entry = True
    for number_info in things_to_trim:
        for coord in number_info[1]:
            y, x = coord[0], coord[1]
            pboard[y][x].remove(number_info[0])
            if first_entry:
                first_entry = False
                GAMESTEPS[0] += 1
                display.append((coord, number_info[0], "remove"))
            else:
                display = [(coord, number_info[0], "remove")]
            msg = " because its seen by all members of the hinged " + x_length_lookup[x_length]
            display_msg = "Removed " + str(number_info[0]) + msg
            support.update_gamestepslog('pboard', 'remove', coord, number_info[0], display_msg, False, display)


def find_hinged_quads(pboard, max_length):
    ''' written to support any length hinged match... I will only call it for size 4 though '''
    keys = find_keys(pboard, max_length)
    for key in keys:
        #log(0, "the key is " + str(key))
        key_seen_coords = seen_coords(pboard, key)
        corners = []
        for coord in key_seen_coords:
            y, x = coord[0], coord[1]
            if 2 <= len(pboard[y][x]) <= max_length:
                corners.append(coord)
        if len(corners) >= max_length - 1:
            cornersets = create_set_iterable(max_length - 1, len(corners))
            for cornerset in cornersets:
                #log(0, cornerset)
                possibilities = set()
                real_corners = [key]
                for i in cornerset:
                    real_corners.append(corners[i])
                #log(0, real_corners)
                for corner in real_corners:
                    for num in pboard[corner[0]][corner[1]]:
                        possibilities.add(num)
                if len(possibilities) == max_length:
                    #log(0, possibilities)
                    not_restricted_nums = find_non_restricted_nums(pboard, possibilities, real_corners)
                    if not_restricted_nums:
                        things_to_trim = find_common_coord(pboard, not_restricted_nums)
                        if things_to_trim:
                            trim_and_report(pboard, things_to_trim, real_corners, max_length, key)
                            return True
    return False

def hinged_quad(board, pboard):
    ''' Finds hinged quads '''
    if find_hinged_quads(pboard, 4):
        return True
    else:
        return False
hinged_quad.name = "Hinged Quad"
