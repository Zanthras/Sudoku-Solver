
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


from s_globals import *
from s_info import get_coord_list, unshared_copy, cflip

#---------------------------Web Presentation functions---------------------------


def publish_table(steps):
    ''' support for ptable '''
    board = init_board
    pboard = unshared_copy(blank_pboard)
    # silently do all the work up to but not including the current step
    for step in range(steps):
        for entry in GAMESTEPSLOG:
            y, x = entry[3][0], entry[3][1]
            if entry[0] == step:
                if entry[1] == 'board':
                    if entry[2] == 'add':
                        board[y][x] = entry[4]
                if entry[1] == 'pboard':
                    if entry[2] == 'add':
                        pboard[y][x].append(entry[4])
                    if entry[2] == 'remove':
                        pboard[y][x].remove(entry[4])
    # special considerations for the current step, we only add, we do not remove
    for entry in GAMESTEPSLOG:
        y, x = entry[3][0], entry[3][1]
        if entry[0] == steps:
            if entry[1] == 'board':
                if entry[2] == 'add':
                    board[y][x] = entry[4]
            STEP_COLOR_INFO.extend(entry[6])
    # show a blank board when there is nothing on the board
    if board == blank_board:
        print tableprint(board, blank_pboard)
    else:
        print tableprint(board, pboard)



rowbegin = [1,4,7]
rowmiddle = [2,5,8]
rowend = [3,6,9]

colordict = {
'add' : "43E041",
'remove' : "FE2E64",
'set1' : "F4FA58",
'set2' : "58ACFB",
}

def cellprint(cell, big, coord, bgcolor="FFFFFF"):
    if big:
        for entry in STEP_COLOR_INFO:
            if entry[0] == coord and entry[1] == cell:
                bgcolor = colordict[entry[2]]
        html = '\n          <td class="bigcell" onmouseover=window.status=\'{}\' onmouseout=window.status="" bgcolor="#{}">'.format(str(cflip(coord)).replace(" ", ""), bgcolor)
        html += str(cell)
        html += '</td>'
        return html
    else:
        html = '\n          <td onmouseover=window.status=\'{}\' onmouseout=window.status="">\n            <table class="ptable">\n'.format(str(cflip(coord)).replace(" ", ""))
        for number in range(1,10):
            bgcolor="FFFFFF"
            if number in rowbegin:
                cellid = "pcelll"
            if number in rowmiddle:
                cellid = "pcellc"
            if number in rowend:
                cellid = "pcellr"
            for entry in STEP_COLOR_INFO:
                if entry[0] == coord and entry[1] == number and number in cell:
                    bgcolor = colordict[entry[2]]
            if number in rowbegin:
                html += '              <tr>\n'
            html += '                <td class="' + cellid + '" bgcolor="#' + bgcolor + '">' 
            if number in cell:
                html += str(number)
            else:
                html += "&nbsp;"
            html += '</td>\n'
            if number in rowend:
                html += '              </tr>\n'
        html += '            </table>\n          </td>'
        return html

def squareprint(board, pboard, coords):
    html = '\n    <td>\n      <table border="1" cellpadding="1" cellspacing="1">'
    count = 0
    for c in coords:
        count += 1
        if count in rowbegin:
            html += "\n        <tr>"
        if int(board[c[0]][c[1]]) != 0:
            html += cellprint(board[c[0]][c[1]], True, c)
        else:
            html += cellprint(pboard[c[0]][c[1]], False, c)
        if count in rowend:
            html += "\n        </tr>"
    html += "\n      </table>\n    </td>"
    return html


def tableprint(board, pboard):
    count = 0
    html = '<table><tr><td></td><td><img src="topaxis.png" border="0"/></td></tr><tr><td><img src="sideaxis.png" border="0"/></td><td>\n<table>'
    for square in range(9):
        count += 1
        coords = get_coord_list(square, 2)
        if count in rowbegin:
            html += "\n  <tr>"
        html += squareprint(board, pboard, coords)
        if count in rowend:
            html += "\n  </tr>"
    html += "\n</table>\n</td></tr></table>"
    return html
 
