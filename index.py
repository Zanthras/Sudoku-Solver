#!/Python27/python

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

print('Content-type: text/html\r\n\r')
print'<meta http-equiv="Content-Type" content="text/html;charset=utf-8">'
print "<title>Sudoku Solver by Zan</title>"
#print'<link rel="shortcut icon" href="http://example.com/myicon.ico" />'



import sys

import cgi
import cgitb
import os

import operator

import examples

# empty log from previous run
try:
    os.remove("sudoku.log")
except:
    pass

import sudoku

# debugging
cgitb.enable()


SOLVED = False
STEPMODE = True
Solve_step = 0

form = cgi.FieldStorage()
options = form.keys()
if "solveit" in options:
    SOLVED = True
    STEPMODE = False
for i in range(len(options)):
    if "step" in options[i]:
        if "step" in form.keys()[i]:
            key = form.keys()[i]
        steps = key.split(":")
        if int(steps[1]) <= 0:
            Solve_step = 0
        else:
            Solve_step = int(steps[1])

if "example" in options or "id" in options:
    if "example" in options:
        boardidname = form["example"].value
        if boardidname in examples.boards:
            boardid = examples.boards[boardidname]
            user_board, bID = sudoku.seed_array_from_http_get(boardid)
            boardidurl = "?id=" + bID
        else:
            boardidurl = ''
            user_board, bID = sudoku.seed_array_from_http_get(boardidurl)
    if "id" in options:
        boardid = form["id"].value
        user_board, bID = sudoku.seed_array_from_http_get(boardid)
        boardidurl = "?id=" + bID
else:
    boardidurl = ''
    user_board, bID = sudoku.seed_array_from_http_get(boardidurl)
    
    
print '''
<style>
#board {float:left;}

#gamelog {
overflow-y:auto;
height:480px;
}

#inputform {
    width:300px;
    float:left;
}

#stats {
    width:500px;
    height:200px;
    float:left;
}

.bigcell {
width:47px;
height:51px;
text-align:center;
font-size:xx-large;
}

.pcelll {
width:11px;
text-align:left;
}

.pcellr {
width:11px;
text-align:right;
}

.pcellc {
width:11px;
text-align:center;
}

.ptable {
width:47px;
line-height:.7;
}

</style>
'''

print '<div id="board">'

if STEPMODE:
    sudoku.main(Solve_step, user_board, oo=True)
    maxsteps = sudoku.GAMESTEPS[0]

if SOLVED:
    Solve_step = 999
    sudoku.SOLVE.append(True)
    sudoku.main(Solve_step, user_board, oo=True)
    maxsteps = sudoku.GAMESTEPS[0]
    Solve_step = maxsteps
# check to prevent the steps from going beyond the end after the board is complete/failed
if sudoku.STEPSREQUIRED[0] != 0:
    if maxsteps < Solve_step:
        Solve_step = maxsteps

def step_calc(increment):
    # if the puzzle isnt solved increment normally??
    if sudoku.STEPSREQUIRED[0] == 0:
        return str(Solve_step + increment)
    else:
        return str(min(sudoku.STEPSREQUIRED[0], Solve_step + increment))

print '<div style="text-align:center">'
print '<form action="index.py%s" method="post">' % boardidurl
print '<input type="submit" name="step:%s" value="<< Back"/>' % str(max(0, Solve_step - 5))
print '<input type="submit" name="step:%s" value="< Back"/>' % str(max(0,Solve_step - 1))
print '<input type="submit" name="solveit" value="Solve"/>'
print '<input type="submit" name="restart" value="Restart"/>'
print '<input type="submit" name="step:%s" value="Next >"/>' % step_calc(1)
print '<input type="submit" name="step:%s" value="Next >>"/>' % step_calc(5)
print '</form>'
print '</div></div>'

print '<div><table><tr><td>'


print '<font size=4> GameLog for step: %s</font> <br>' %str(Solve_step)
print '</td></tr><tr><td><div id="gamelog">'
if len(sudoku.WEB_GAMELOG[0]) == 0:
    pass
else:
    for entry in sudoku.WEB_GAMELOG:
        print entry
print '</div></td></tr></table></div>'

print '<div id="upload">'

print '''
<br><br><br><br>
Enter your starting board in the box and click set board. as long as you enter 81 numbers it will attempt to solve those numbers, 0's are blank.
Or select an example board from the dropdown menu and click set board<br><br>
<br>
<div id="inputform">
<form name="input" action="index.py" method="get">

<textarea cols="9" rows="9" maxlength="200" name="id">
</textarea>
<br>
<select name="example">
<option value="userinput">Examples</option>
'''

for entry in examples.boards:
    print '<option value="' + entry + '">' + entry + '</option>'

'''
<option value="easy">Easy</option>
<option value="medium">Medium</option>
<option value="hard">Hard</option>
<option value="hard2">Hard 2</option>
<option value="veryhard">Very Hard</option>
<option value="veryhard2">Very Hard 2</option>
<option value="veryhard3">Very Hard 3</option>
'''

print '''
<select>
<input type="submit" value="Set Board">
</form>
</div>
<div id="stats">
'''
if len(sudoku.SOLVER_STATS) > 0:
    print "Solver Stats:<br>"
    for entry in sorted(sudoku.SOLVER_STATS, key=sudoku.SOLVER_STATS.get, reverse=True):
        print entry, sudoku.SOLVER_STATS[entry], "<br>"


print '''
</div>
</div>
'''

print '<br><br><br><br><br><br><br><br><br><br><br><br><a href="index.py">Main</a> <a href="changelog.txt">Changelog</a> <a href="sudoku.log">Log</a> <a href="source/">Source</a>'



    
