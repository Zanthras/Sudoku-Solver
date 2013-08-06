
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
import logging

from s_globals import *
from s_info import *


#---------------------------support functions---------------------------


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
    if int(websteps) == GAMESTEPS[0]:
        log(1, "Stopping solve at step %s" % websteps )
        final = True
    complete = True
    for row in board:
        if 0 in row:
            complete = False
    if complete or final:
        write_webgamelog(GAMESTEPSLOG, websteps)
        STEPSREQUIRED[0] = GAMESTEPS[0]
        return complete


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


def oo_update_actions(coord, num, board, pboard):
    board[coord[0]][coord[1]] = num
    msg = "placed the number " + str(num)
    display = [(coord, num, 'add')]
    update_gamestepslog('board', 'add', coord, num, msg, False, display)
    loop_optimize(num, coord)
    trim_possibility_table_from_board_update(coord, num, pboard)


def trim_possibility_table_from_board_update(coordinate, number, pboard):
    ''' trims the basics after an update '''
    coord_list = []
    # clean updated coord, and all related coords
    pboard[coordinate[0]][coordinate[1]] = []
    for x_type in range(3):
        coord_list = get_coord_list(coordinate, x_type)
        for coord in coord_list:
            y, x = coord[0], coord[1]
            if number in pboard[y][x]:
                pboard[y][x].remove(number)
                msg = 'Trimmed the ' + trim_type_lookup[x_type] + ' of ' + str(number)
                display = [(coord, number, 'remove')]
                update_gamestepslog('pboard', 'remove', coord, number, msg, False, display)

