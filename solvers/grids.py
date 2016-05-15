
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

''' Main Sudoku application expects the solve functions to take only board, and pboard as their inputs hence the need for 2 controlling functions based off length of the grid '''

def quad_grid(board, pboard):
    ''' Solves for 4x4 Grids returns a boolean indicating work done'''
    x_length = 4
    return gridtacular(pboard, x_length)
quad_grid.name = "Quad Grid"

def trip_grid(board, pboard):
    ''' Solves for 3x3 Grids returns a boolean indicating work done'''
    x_length = 3
    return gridtacular(pboard, x_length)
trip_grid.name = "Triple Grid"


def gridtacular(pboard, x_length):
    ''' Solves for variable size grids returns a boolean indicating work done '''
    for number in NUMBERS:
        for x_type in range(2):
            data_array = []
            # Each line should contain between 1 and x_length of my number to be considered
            for line in LINES[x_type]:
                potential_line = []
                coords = get_coord_list(line, x_type)
                for coord in coords:
                    y, x = coord[0], coord[1]
                    if number in pboard[y][x]:
                        potential_line.append(coord)
                if len(potential_line) > 0:
                    if len(potential_line) <= x_length:
                        data_array.append(list(potential_line))
            # I need at least my x_length worth of lines to attempt to make a grid
            if len(data_array) >= x_length:
                possible_combinations = create_set_iterable(x_length, len(data_array))
                for combination in possible_combinations:
                    grid_info = is_a_grid(data_array, combination, x_type)
                    if grid_info:
                        trimmed = trim_grid(pboard, number, grid_info, x_type)
                        if trimmed:
                            GAMESTEPS[0] += 1
                            msg = "Removed " + str(number) + " as its seen by the " + trim_type_lookup[x_type] + " based grid"
                            display = []
                            for grid_coord in grid_info[0]:
                                display.append((grid_coord, number, "set1"))
                            for coord in trimmed:
                                otl = list(display)
                                otl.append((coord, number, "remove"))
                                support.update_gamestepslog('pboard', 'remove', coord, number, msg, False, otl)
                            # Stop looping completely, because there was something to trim
                            return True
                    else:
                        continue
    # Nothing at all found, im done
    return False


def create_set_iterable(x_length, number_of_lines):
    ''' Returns a set (of the size x_length) of all unique combinations of the numbers (number_of_lines) 
    example of 4 lines length of 3: [012, 013, 023, 123]
    '''
    iterable = []
    current_line_set = range(x_length)
    iterable.append(list(current_line_set))
    while increment_line_set(current_line_set, number_of_lines, x_length):
        iterable.append(list(current_line_set))
    return iterable

def increment_line_set(cur_set, number_of_lines, x_length):
    ''' Will increment cur_set by one, or return False if it cant be incremented '''
    if cur_set == max_set(number_of_lines, x_length):
        return False
    position = x_length - 1
    while True:
        max_number_for_position = number_of_lines - (x_length - position)
        if cur_set[position] < max_number_for_position:
            increment(cur_set, position, number_of_lines, x_length)
            return cur_set
        else:
            position -= 1

def max_set(number_of_lines, x_length):
    ''' Returns the last set of lines '''
    max_setnums = []
    while True:
        if len(max_setnums) == x_length:
            return max_setnums[::-1]
        number_of_lines -= 1
        max_setnums.append(number_of_lines)

def increment(cur_set, position_to_start, number_of_lines, x_length):
    ''' Increments the cur_set by one starting at the position_to_start '''
    num = 0
    for i in range(len(cur_set)):
        if i == position_to_start:
            cur_set[i] += 1
            num = cur_set[i]
        if i > position_to_start:
            num += 1
            cur_set[i] = num


def is_a_grid(data_array, combo, x_type):
    ''' Given a combonation of lines, a data_array and the grid type (x_type), checks if its a grid and returns either a boolean of False or the grid definition '''
    xset = set()
    yset = set()
    grid_coords = []
    for line in combo:
        for coord in data_array[line]:
            grid_coords.append(coord)
            yset.add(coord[0])
            xset.add(coord[1])
    # combo is half the grid definition, return_set is the other half (rows vs columns)
    if x_type == 0:
        return_set = xset
    if x_type == 1:
        return_set = yset
    if len(xset) == len(yset):
        return grid_coords, return_set
    else:
        return False

def trim_grid(pboard, number, grid_info, x_type):
    ''' Given a grid, attempt to trim it, returns a list of things trimmed '''
    grid_coords, alt_lines = grid_info[0], grid_info[1]
    if x_type:
        alt_xtype = 0
    else:
        alt_xtype = 1
    trimmed = []
    # Grid is defined by the lack of excess in the primary direction, can only trim the alt direction
    for line in alt_lines:
        coords = get_coord_list(line, alt_xtype)
        for coord in coords:
            y, x = coord[0], coord[1]
            # Dont trim the grid itself
            if coord not in grid_coords:
                if number in pboard[y][x]:
                    pboard[y][x].remove(number)
                    trimmed.append(coord)
    return trimmed