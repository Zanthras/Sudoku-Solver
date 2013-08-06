
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
from grids import create_set_iterable
from s_info import *
from s_globals import *

def line_trim(pboard, line_coords, matched_coords, trimmed, poss_set):
    ''' Removes matched numbers from the unmatched coords'''
    for line_coord in line_coords:
        if line_coord not in matched_coords:
            for trim_num in poss_set:
                if trim_num in pboard[line_coord[0]][line_coord[1]]:
                    trimmed.append((line_coord, trim_num))
                    pboard[line_coord[0]][line_coord[1]].remove(trim_num)


def match_trim(pboard, match_nums, match_coords, trimmed):
    ''' Removes excess numbers from the matched coords'''
    for coord in match_coords:
        y, x = coord[0], coord[1]
        nums = list(pboard[y][x])
        for num in nums:
            if num not in match_nums:
                pboard[y][x].remove(num)
                trimmed.append((coord, num))


def look_for_matches_from_dict(coord_dict, x_length):
    ''' returns a list of numbers that constitute a hidden match '''
    possible_list = []
    matches = []
    for entry in coord_dict:
        if 2 <= len(coord_dict[entry]) <= x_length:
            possible_list.append(entry)
    if len(possible_list) >= x_length:
        unique_sets  = create_set_iterable(x_length, len(possible_list))
        for unique_set in unique_sets:
            # make a list of my hidden match for easier lookup later
            hidden_match = []
            hidden_match_coord_set = set()
            for i in unique_set:
                hidden_match.append(possible_list[i])
            for number in hidden_match:
                for d_coord in coord_dict[number]:
                    hidden_match_coord_set.add(d_coord)
            if len(hidden_match_coord_set) == x_length:
                matches.append([hidden_match_coord_set, hidden_match])
    if len(matches) > 0:
        return matches
    else:
        return False
 
def trim_cleanup(pboard, matched_coords, match_nums, trimmed_list, msg):
    first_entry = True
    display = []
    for coord in matched_coords:
        y, x = coord[0], coord[1]
        for num in pboard[y][x]:
            if num in match_nums:
                display.append((coord, num, "set1"))
    for entry in trimmed_list:
        if first_entry:
            first_entry = False
            GAMESTEPS[0] += 1
            display.append((entry[0], entry[1], "remove"))
        else:
            display = [(entry[0], entry[1], "remove")]
        display_msg = "Removed " + str(entry[1]) + msg
        support.update_gamestepslog('pboard', 'remove', entry[0], entry[1], display_msg, False, display)

def hidden_matches(board, pboard,):
    ''' Looks for matched x_length entries to trim the rest of the line '''
    x_lenth_lookup = { 2:"pair", 3:"triplicate"}
    for x_type in range(3):
        for x_length in range(2, 4):
            for line in LINES[x_type]:
                coord_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
                line_coords = list(get_coord_list(line, x_type))
                for coord in line_coords:
                    y, x = coord[0], coord[1]
                    for entry in pboard[y][x]:
                        coord_dict[entry].append(coord)
                matches = look_for_matches_from_dict(coord_dict, x_length)
                if matches:
                    for match in matches:
                        match_coords, match_nums = match[0], match[1]
                        trimmed = []
                        match_trim(pboard, match_nums, match_coords, trimmed)
                        if x_type == 0 or x_type == 1:
                            square_coords = get_coord_list(list(match_coords)[0], 2)
                            is_same_square = True
                            for coord in match_coords:
                                if coord not in square_coords:
                                    is_same_square = False
                            #cleanup the rest of the square
                            if is_same_square:
                                line_trim(pboard, square_coords, match_coords, trimmed, match_nums)
                        if trimmed:
                            msg = " because a hidden " + x_lenth_lookup[x_length] + " was found "
                            trim_cleanup(pboard, match_coords, match_nums, trimmed, msg)
                            return True
    return False
hidden_matches.name = "Hidden Match"
