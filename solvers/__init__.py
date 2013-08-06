
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

from singles import solve_singles
from singleposs import solve_single_possible
from match import hidden_matches
from naked import naked_entries
from related import related_trips
from pointing import line_pointing
from chains import simple_chain, complex_chain
from update import trim_possibility_table_from_board_update
from corner import corner_intersect
from locked_pairs import locked_pairs
from grids import quad_grid, trip_grid
from medusa import medusa_chain
from hinged import hinged_match
from quadhinged import hinged_quad
