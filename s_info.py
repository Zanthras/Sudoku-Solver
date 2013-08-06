
# coding=utf-8

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

import time
import sys
import datetime
import logging

from s_globals import *

#---------------------------LOOKUP/GET INFO FUNCTIONS---------------------------

def get_small_square_list(number, board):
    ''' returns a list of numbers in the specified square '''
    returnlist = []
    if number in list1:
        row = list1
    elif number in list2:
        row = list2
    elif number in list3:
        row = list3
    if number in list4:
        column = list1
    elif number in list5:
        column = list2
    elif number in list6:
        column = list3
    for y in row:
        for x in column:
            returnlist.append(board[y][x])
    return returnlist

def get_column_list(column, board):
    ''' returns a list of numbers in the specified column '''
    returnlist = []
    for i in range(9):
        returnlist.append(board[i][column])
    return returnlist

def get_row_list(row, board):
    ''' returns a list of numbers in the specified row '''
    return board[row]

def generate_array_coord(square, number):
    ''' given a index from a square_num_list and the square return the y,x coords '''
    if square in list1:
        rows = list1
    elif square in list2:
        rows = list2
    elif square in list3:
        rows = list3
    if square in list4:
        columns = list1
    elif square in list5:
        columns = list2
    elif square in list6:
        columns = list3
    if number in list1:
        row = rows[0]
    elif number in list2:
        row = rows[1]
    elif number in list3:
        row = rows[2]
    if number in list4:
        column = columns[0]
    elif number in list5:
        column = columns[1]
    elif number in list6:
        column = columns[2]
    return row, column


def lookup_array_coord(square, number):
    ''' given a index from a square_num_list and the square return the y,x coords '''
    return coord_array[(square, number)]

def lookup_square_from_coords(coords):
    ''' Given coords (y,x) return the square it belongs to '''
    if coords[0] in list1:
        y = list1
    elif coords[0] in list2:
        y = list2
    elif coords[0] in list3:
        y = list3
    if coords[1] in list1:
        x = list4
    elif coords[1] in list2:
        x = list5
    elif coords[1] in list3:
        x = list6
    return list(set(y) & set(x))[0]

def get_coord_list(invalue, type_x):
    ''' returns list of coords for thing row/column/square '''
    #type_x_lookup = {0:"row", 1:"column", 2:"square"}
    if isinstance(invalue, tuple):
        if type_x == 0:
            value = invalue[0]
        if type_x == 1:
            value = invalue[1]
        if type_x == 2:
            value = lookup_square_from_coords(invalue)
    else:
        value = invalue    
    return coord_list_array[(type_x, value)]

def generate_coord_list(invalue, type_x):
    ''' returns list of coords for thing row/column/square '''
    type_x_lookup = {0:"row", 1:"column", 2:"square"}
    if isinstance(invalue, int):
        value = (invalue, invalue)
    else:
        value = invalue
    returnlist = []
    if type_x == 0:
        for i in range(9):
            returnlist.append((value[0], i))
    if type_x == 1:
        for i in range(9):
            returnlist.append((i, value[1]))
    if type_x == 2:
        for number in range(9):
            returnlist.append(lookup_array_coord(invalue, number))
    return returnlist

coord_array = {}
for square in range(9):
    for number in range(9):
        key = (square, number)
        coord = generate_array_coord(square, number)
        coord_array[key] = coord

coord_list_array = {}
for type in range(3):
    for num in range(9):
        key = (type, num)
        coord_list = generate_coord_list(num, type)
        coord_list_array[key] = coord_list

def cflip(c):
    y = c[0]
    x = c[1]
    y += 1
    x += 1
    return (x,y)


def coord_from_list(pboard, input_list):
    for y in range(9):
        for x in range(9):
            if id(pboard[y][x]) == id(input_list):
                return (y, x)


def unshared_copy(inList):
    if isinstance(inList, list):
        return list( map(unshared_copy, inList) )
    return inList


# logging config
logging.basicConfig(format='%(asctime)s -%(levelname)s- %(message)s', datefmt='%m/%d/%Y %I:%M:%S', filename='sudoku.log', level=logging.DEBUG, )
    
def log(facility, msg):
    '''facility 0 = debug, 1 = info, 2 = warning, 3 = error, 4 = critical '''
    if facility == 0:
        logging.debug(msg)
    if facility == 1:
        logging.info(msg)
    if facility == 2:
        logging.warn(msg)
    if facility == 3:
        logging.error(msg)
    if facility == 4:
        logging.critical(msg)

#---------------------------support functions---------------------------

# I need to engineer this somehow to not be in the info module... it doesnt belong here

def loop_optimize(number, coord):
    if number != 0:
        square = lookup_square_from_coords(coord)
        NUMS_COUNT[number] += 1
        ROWS_SUM[coord[0]] += 1
        COLS_SUM[coord[1]] += 1
        SQUS_SUM[square] += 1 
        if NUMS_COUNT[number] == 9:
            NUMBERS.remove(number)
            #print "number", number, "is complete"
        if ROWS_SUM[coord[0]] == 9:
            ROWS.remove(coord[0])
            #print "row", coord[0], "is complete"
        if COLS_SUM[coord[1]] == 9:
            COLUMNS.remove(coord[1])
            #print "column", coord[1], "is complete"
        if SQUS_SUM[square] == 9:
            SQUARES.remove(square)
            #print "square", square, "is complete"


def seed_array_from_http_get(url):
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    sanitised = ''
    if len(url) >= 81 and len(url) < 200:
        for char in url:
            if char in nums:
                sanitised += char
    else:
        sanitised = "0" * 81
    board = unshared_copy(blank_board)
    i = 0
    for y in range(9):
        for x in range(9):
            number = int(sanitised[i])
            board[y][x] = number
            loop_optimize(number, (y,x))
            i += 1
    return board, sanitised
    





def oo_is_done(board, pboard, websteps, final=False):
    #  Stop solving if I dont need to solve further
    # complete means the puzzle has been solved
    # final means  i couldnt solve the puzzle
    # stopped means the puzzel was stopped by user request (ie they only want to see up to step x)
    # complete should prevent step progress
    # final should prevent step progress
    # stopped should NOT prevent step progress
    stopped = False
    if int(websteps) == GAMESTEPS[0]:
        log(1, "Stopping solve at step %s" % websteps )
        final = True
        stopped = True
    complete = True
    for row in board:
        if 0 in row:
            complete = False
    if complete or final:
        write_webgamelog(GAMESTEPSLOG, websteps)
        if not stopped:
            # This will prevent step progress
            STEPSREQUIRED[0] = GAMESTEPS[0]
        return True



def is_board_complete(board, pboard, steps):
    complete = True
    for row in board:
        if 0 in row:
            complete = False
    if complete:
        write_webgamelog(GAMESTEPSLOG, steps)
        return complete

    
def update_gamestepslog(b_type, func, coord, num, msg, step_up, table_format=[]):
    if step_up:
        GAMESTEPS[0] += 1
    step = GAMESTEPS[0]
    GAMESTEPSLOG.append([step, b_type, func, coord, num, msg, table_format])

    
def write_webgamelog(log, steps):
    formatted = ''
    if SOLVE:
        for line in log:
            if int(line[0]) <= steps and int(line[0]) != 0:
                if line[2] != 'info':
                    formatted += "At " + str(cflip(line[3])) + ': ' + line[5] + "<br>"
                if line[2] == 'info':
                    if len(line[5]) > 0:
                        formatted += line[5] + '<br>'
    else:
        for line in log:
            if int(line[0]) == steps and int(line[0]) != 0:
                if line[2] != 'info':
                    formatted += "At " + str(cflip(line[3])) + ': ' + line[5] + "<br>"
                if line[2] == 'info':
                    if len(line[5]) > 0:
                        formatted += line[5] + '<br>'
    WEB_GAMELOG[0] = formatted
