
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


def naked_entries(board, pboard):
    for trim_type in range(3):
        for x_length in range(2, 4):
            if trim_naked_matches(pboard, trim_type, x_length):
                return True
    return False
naked_entries.name = "Naked Entries"


def extra_check(coords, matched, trim_type,):
    ''' If I find a naked match, check to see if its a match in another way (such as both a row and a square) '''
    # Only need to check if row or column, not the reverse as i always check the square last
    if trim_type == 0 or trim_type == 1:
        s_coords = get_coord_list(matched[0], 2)
        is_square = True
        for match_coord in matched:
            if match_coord not in s_coords:
                is_square = False
        if is_square:   
            #log(0, "extra check found square")
            return coords + s_coords
    return coords


def trim_naked_matches(pboard, trim_type, x_length):
    trim_type_lookup = {0:"row", 1:"column", 2:"square",}
    x_lenth_lookup = { 2:"pair", 3:"triplicate"}
    any_trim = False
    results = naked_matches(pboard, trim_type, x_length)
    if results[0]:
        for result in results[1]:
            dedup = False
            matched, line = result[0], result[1]
            matched_nums = []
            m_c = matched[0]
            for num in pboard[m_c[0]][m_c[1]]:
                matched_nums.append(num)
            coordinates = get_coord_list(line, trim_type)
            # replace with my extra check set of coords
            coordinates = extra_check(coordinates, matched, trim_type,)
            for number in matched_nums:
                for c in coordinates:
                    if c not in matched:
                        if number in pboard[c[0]][c[1]]:
                            any_trim = True
                            pboard[c[0]][c[1]].remove(number)
                            #print "removed", number, "from", c
                            c_list = ''
                            for e in matched:
                                c_list += str(cflip(e)) + ' '
                            msg = "Trimmed " + str(number) + " due to naked " + x_lenth_lookup[x_length] + " at " + c_list
                            displaystuff = []
                            for numbers in matched_nums:
                                displaystuff.append((matched[0], numbers, "set1"))
                                displaystuff.append((matched[1], numbers, "set1"))
                            displaystuff.append((c, number, "remove"))
                            if dedup:
                                support.update_gamestepslog('pboard', 'remove', c, number, msg, False, displaystuff)
                            else:
                                support.update_gamestepslog('pboard', 'remove', c, number, msg, True, displaystuff)
                            dedup = True
    return any_trim


def naked_matches(pboard, trim_type, x_length):
    ''' Looks for naked matched x_length entries to trim the rest of the line '''
    naked_matched = []
    for line in LINES[trim_type]:
        coordinates = get_coord_list(line, trim_type)
        poss_naked = []
        for c in coordinates:
            if len(pboard[c[0]][c[1]]) == x_length:
                poss_naked.append(c)
        for entry in poss_naked:
            count = 0
            matched = []
            for compare in poss_naked:
                if pboard[entry[0]][entry[1]] == pboard[compare[0]][compare[1]]:
                    count += 1
                    matched.append(compare)
            if count == x_length:
                if (matched, line) not in naked_matched:
                    naked_matched.append((matched, line))
    if len(naked_matched) != 0:
        return True, naked_matched
    else:
        return False, []
