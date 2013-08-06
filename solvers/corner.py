
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


def debuglog(key, msg):
    if key == (1, 5):
        log(0, msg)


def create_key_list(pboard):
    key_list = []
    for row in ROWS:
        coords = get_coord_list(row, 0)
        for c in coords:
            if len(pboard[c[0]][c[1]]) == 2:
                key_list.append(c)
    return key_list

def coord_map(coord):
    coords = set()
    for xtype in range(3):
        line_coords = get_coord_list(coord, xtype)
        for c in line_coords:
            coords.add(c)
    coords.remove(coord)
    return coords

def corner_intersect(board, pboard):
    keys = create_key_list(pboard)
    #log(0, keys)
    for key in keys:
        #debuglog(key, "checking key " + str(cflip(key)))
        seen_coords = set()
        for xtype in range(3):
            coords = get_coord_list(key, xtype)
            for coord in coords:
                # filter for only 2 length ptables... hey I made this filter already.
                if coord in keys:
                    seen_coords.add(coord)
        # I dont want to include myself
        seen_coords.remove(key)
        #debuglog(key, seen_coords)
        # build up a list of potential corners
        corner1_list = []
        corner1_altset = set()
        corner2_list = []
        corner2_altset = set()
        first_num = True
        for num in pboard[key[0]][key[1]]:
            for pcorner in seen_coords:
                y, x = pcorner[0], pcorner[1]
                if num in pboard[y][x]:
                    templist = list(pboard[y][x])
                    templist.remove(num)
                    if first_num:
                        corner1_list.append(pcorner)
                        corner1_altset.add(templist[0])
                    else:
                        corner2_list.append(pcorner)
                        corner2_altset.add(templist[0])
            if first_num:
                first_num = False
        # look for potential common alternate numbers
        alts = corner1_altset & corner2_altset
        for alt in alts:
            #debuglog(key, "I found the alt " + str(alt))
            # define my possible corners (I can find more than one match)
            corner1_possible = []
            corner2_possible = []
            for c1coord in corner1_list:
                y, x = c1coord[0], c1coord[1]
                if alt in pboard[y][x]:
                    corner1_possible.append(c1coord)
                    #debuglog(key, "corner 1 possible is " + str(cflip(c1coord)))
            for c2coord in corner2_list:
                y, x = c2coord[0], c2coord[1]
                if alt in pboard[y][x]:
                    corner2_possible.append(c2coord)
                    corner2 = c2coord
                    #debuglog(key, "corner 2 possible is " + str(cflip(c2coord)))
            # loop through all corner combinations:
            corners = gen_poss_combos(corner1_possible, corner2_possible)
            for corner_attempt in corners:
                corner1, corner2 = corner_attempt[0], corner_attempt[1]
                # map my seen coord space
                seen_by_c1 = coord_map(corner1)
                seen_by_c2 = coord_map(corner2)
                # safety first... remove the other corner
                if corner2 in seen_by_c1:
                    seen_by_c1.remove(corner2)
                if corner1 in seen_by_c2:
                    seen_by_c2.remove(corner1)
                # define the overlap
                seen_by_both = seen_by_c1 & seen_by_c2
                # check for the alternate number in the intersection
                trimmed = False
                trimmed_list = []
                for coord in seen_by_both:
                    y, x = coord[0], coord[1]
                    if alt in pboard[y][x]:
                        # rejoice!
                        pboard[y][x].remove(alt)
                        trimmed = True
                        trimmed_list.append(coord)
                if trimmed:
                    report(pboard, key, corner1, corner2, trimmed_list, alt)
                    return True
    return False
corner_intersect.name = "Corner Intersection"


def report(pboard, key, corner1, corner2, trimmed_list, alt):
    msg = "Removed " + str(alt) + " due to corner intersection at the corners " + str(cflip(corner1)) + ", " + str(cflip(corner2)) + " and the key " + str(cflip(key))
    GAMESTEPS[0] += 1
    y, x = key[0], key[1]
    num1, num2 = pboard[y][x][0], pboard[y][x][1]
    display = [(key, num1, 'set1'), (key, num2, 'set1'), (corner1, num1, 'set1'), (corner2, num2, 'set1'), (corner1, alt, 'set2'), (corner2, alt, 'set2'),]
    for coord in trimmed_list:
        otl = list(display)
        otl.append((coord, alt, "remove"))
        support.update_gamestepslog('pboard', 'remove', coord, alt, msg, False, otl)

def gen_poss_combos(set1, set2):
    reversed_combos = []
    possible_combos = []
    for left in set1:
        for right in set2:
            if [left, right] not in reversed_combos:
                possible_combos.append([left, right])
                reversed_combos.append([left, right])
                reversed_combos.append([right, left])
    return possible_combos
