
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

def find_binary_pair(pboard, line, xtype, number):
    line_coords = get_coord_list(line, xtype)
    pair = []
    for coord in line_coords:
        y, x = coord[0], coord[1]
        if number in pboard[y][x]:
            pair.append(coord)
    if len(pair) == 2:
        return pair
    else:
        return False

def check_if_square(pboard, altpairs, alt_xtype):
    for apair in altpairs:
        line_coords = get_coord_list(apair[0], alt_xtype)
        if apair[1] not in line_coords:
            return False
    return True

def rotate(pairs, xtype):
    altset1 = [pairs[0][0], pairs[1][0]]
    altset2 = [pairs[0][1], pairs[1][1]]
    altsets = [altset1, altset2]
    if xtype:
        alt_xtype = 0
    else:
        alt_xtype = 1
    return altsets, alt_xtype

def return_pair_combos(pairs):
    if len(pairs) < 2:
        return []
    if len(pairs) == 2:
        return [pairs]
    else:
        combolist = []
        inverse_plus_combolist = []
        for firstpair in pairs:
            for secondpair in pairs:
                if firstpair != secondpair:
                    plist = [firstpair, secondpair]
                    inverseplist = [secondpair, firstpair]
                    if plist not in inverse_plus_combolist:
                        combolist.append(plist)
                        # add to full list so i dont process again
                        inverse_plus_combolist.append(plist)
                        inverse_plus_combolist.append(inverseplist)
        return combolist

def trim_alt_line_in_square(pboard, altpair, alt_xtype, number):
    line_coords = list(get_coord_list(altpair[0], alt_xtype))
    # Dont trim my square itself!
    line_coords.remove(altpair[0])
    line_coords.remove(altpair[1])
    trimmed = []
    for coord in line_coords:
        y, x = coord[0], coord[1]
        if number in pboard[y][x]:
            pboard[y][x].remove(number)
            trimmed.append(coord)
    return trimmed


def locked_pairs(board, pboard):
    for number in NUMBERS:
        for xtype in range(2):
            # look for 2 binary pairs
            pairs = []
            for line in LINES[xtype]:
                pair = find_binary_pair(pboard, line, xtype, number)
                if pair:
                    pairs.append(pair)
            # enumerate every possible combination of 2 pairs (if you find 3 binary pairs there are 3 possible squares)
            combopairs = return_pair_combos(pairs)
            if combopairs:
                for combo in combopairs:
                    #log(0, "checking combo" + str(combo))
                    altpairs, alt_xtype = rotate(combo, xtype)
                    if check_if_square(pboard, altpairs, alt_xtype):
                        trimmed = []
                        for altpair in altpairs:
                            trimmed += trim_alt_line_in_square(pboard, altpair, alt_xtype, number)
                        if trimmed:
                            GAMESTEPS[0] += 1
                            locked_pairs = [cflip(combo[0][0]), cflip(combo[0][1]), cflip(combo[1][0]), cflip(combo[1][1]),]
                            msg = "Removed " + str(number) + " because of the locked pairs at " + str(locked_pairs)[1:-1]
                            display = [(combo[0][0], number, "set1"), (combo[0][1], number, "set1"), (combo[1][0], number, "set1"), (combo[1][1], number, "set1")]
                            # fill in the rest of the reporting details laters
                            for coord in trimmed:
                                otl = list(display)
                                otl.append((coord, number, "remove"))
                                support.update_gamestepslog('pboard', 'remove', coord, number, msg, False, otl)
                            return True
    return False
locked_pairs.name = "Locked Pairs"


