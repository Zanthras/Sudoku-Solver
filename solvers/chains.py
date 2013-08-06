
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

def simple_chain(board, pboard):
    type = "simple"
    for number in NUMBERS:
        if trim_ptable_from_chains(pboard, number, type):
            return True
    return False
simple_chain.name = "Simple Chains"

def complex_chain(board, pboard):
    type = "complex"
    for number in NUMBERS:
        if trim_ptable_from_chains(pboard, number, type):
            return True
    return False
complex_chain.name = "Complex Chains"

def find_strong_binary_link(pboard, coord, number, x_type):
    binary_coords = []
    coords = get_coord_list(coord, x_type)
    for c in coords:
        if number in pboard[c[0]][c[1]]:
            binary_coords.append(c)
    if len(binary_coords) == 2:
        return True, binary_coords
    else:
        return False, []
    
def find_weak_binary_link(pboard, coord, number, x_type):
    binary_coords = []
    if x_type == 2:
        coords = get_coord_list(lookup_square_from_coords(coord), x_type)
    else:
        coords = get_coord_list(coord, x_type)
    for c in coords:
        if c != coord:
            if number in pboard[c[0]][c[1]]:
                binary_coords.append(c)
    if len(binary_coords) > 0:
        return True, binary_coords
    else:
        return False, []

def invalid_chain_board(alist, blist):
    lists = [alist, blist]
    for chain in lists:
        rows = set()
        columns = set()
        squares = set()
        for coord in chain:
            rows.add(coord[0])
            columns.add(coord[1])
            squares.add(lookup_square_from_coords(coord))
        if len(rows) != len(chain):
            return True, chain
        if len(columns) != len(chain):
            return True, chain
        if len(squares) != len(chain):
            return True, chain
    return False, []

def find_excess_chain_board(pboard, alist, blist, number):
    othercoord = []
    excess = set()
    for y in range(9):
        for x in range(9):
            coord = (y,x)
            if number in pboard[y][x]:
                if coord not in alist and coord not in blist:
                    othercoord.append(coord)
    for coord in othercoord:
        seeA = False
        seeB = False
        linecds = []
        for x_type in range(3):
            linecds.extend(get_coord_list(coord, x_type))
        count = 0
        for linecd in linecds:
            if linecd in alist:
                seeA = True
            if linecd in blist:
                seeB = True
        if seeA and seeB:
            excess.add(coord)
    return list(excess)

def trim_ptable_from_chains(pboard, number, type):
    any_trim = False
    if type == "simple":
        chained = find_all_simple_chain(pboard, number)
    if type == "complex":
        chained = find_chain_board(pboard, number)
    if chained[0]:
        for chain in chained[1]:
            alist, blist = chain[0], chain[1]
            display = []
            for coord in alist:
                display.append((coord, number, 'set1'))
            for coord in blist:
                display.append((coord, number, 'set2'))
            invalid = invalid_chain_board(alist, blist)
            displayed = False
            if invalid[0]:
                any_trim = True
                GAMESTEPS[0] += 1
                msg = "Invalid binary chain"
                for c in invalid[1]:
                    onetimelist = [(c, number, 'remove')]
                    display.extend(onetimelist)
                    pboard[c[0]][c[1]].remove(number)
                    support.update_gamestepslog('pboard', 'remove', c, number, msg, False, display)
            excess = find_excess_chain_board(pboard, alist, blist, number)
            excess_trimmed = False
            if len(excess) > 0:
                for c in excess:
                    pboard[c[0]][c[1]].remove(number)
                    excess_trimmed = True
            if excess_trimmed:
                any_trim = True
                msg = "Trimmed excess " + str(number) + " that isnt in the binary chains"
                GAMESTEPS[0] += 1
                for coord in excess:
                    onetimelist = display[:]
                    onetimelist.append((coord, number, 'remove'))
                    support.update_gamestepslog('pboard', 'remove', coord, number, msg, False, onetimelist)
            # If a trime was done stop looping and return true
            if any_trim:
                return any_trim
    # No chain found, no trim is possible
    else:
        return False


def find_all_binary(pboard, number):
    ''' Finds and returns a list of every binary pair '''
    binarycoordpairs = []
    for x_type in range(3):
        for line in LINES[x_type]:
            linecoords = get_coord_list(line, x_type)
            coord_pair = []
            for coord in linecoords:
                y, x = coord[0], coord[1]
                if number in pboard[y][x]:
                    coord_pair.append(coord)
            if len(coord_pair) == 2:
                binarycoordpairs.append(coord_pair)
    if len(binarycoordpairs) > 1:
        return True, binarycoordpairs
    else:
        return False, []


    
def find_binary_start(pboard, number):
    ''' Can improve this so it takes as input previous binary chains, and will attempt to find new starts that have already been processed '''
    for x_type in range(3):
            for line in LINES[x_type]:
                binarycoord = []
                linecoords = get_coord_list(line, x_type)
                for coord in linecoords:
                    if number in pboard[coord[0]][coord[1]]:
                        binarycoord.append(coord)
                if len(binarycoord) == 2:
                    return True, binarycoord
    return False, []

def dlog(number, msg):
    if GAMESTEPS[0] >= 0 and number == 10:
        log(0, msg)

def find_chain_board(pboard, number):
    ''' Adding support for weak links '''
    # find binary state starting point
    binarystart = find_binary_start(pboard, number)
    if binarystart[0]:
        coordtoeval = []
        processedlist = []
        alist = []
        blist = []
        aalist = []
        bblist = []
        stronglist = []
        first = True
        for c in binarystart[1]:
            stronglist.append(c)
            coordtoeval.append(c)
            processedlist.append(c)
            if first:
                first = False
                alist.append(c)
            else:
                blist.append(c)
        dlog(number, GAMESTEPS[0])
        dlog(number, "alist: " + str(cflip(alist[0])))
        dlog(number, "alist: " + str(cflip(blist[0])))
        # pop the position list and mark new binary states adding to the position list
        while len(coordtoeval) > 0:
            #print "==============LOOP START============="
            coord = coordtoeval.pop()
            dlog(number, " ------- looping on coord %s -------- " % str(cflip(coord)))
            for x_type in range(3):
                # look for strong links
                if coord not in stronglist:
                    poss_bin = find_strong_binary_link(pboard, coord, number, x_type)
                    if poss_bin[0]:
                        c0 = poss_bin[1][0] 
                        c1 = poss_bin[1][1] #(this is the aaguy)
                        dlog(number, "found binary" + str(cflip(c0)) + str(cflip(c1)))
                        # only process the entry not already proccessed and add to alt list
                        if c0 not in processedlist:
                            processedlist.append(c0)
                            coordtoeval.append(c0)
                            stronglist.append(c0)
                            if c1 in alist:
                                dlog(number, "adding %s to blist" % str(cflip(c0)))
                                blist.append(c0)
                            if c1 in blist:
                                dlog(number, "adding %s to alist" % str(cflip(c0)))
                                alist.append(c0)
                            # upgrade weak links to strong links and add to alt list
                            if c1 in aalist:
                                dlog(number, "upping " + str(cflip(c1)) + " and adding %s to blist" % str(cflip(c0)))
                                aalist.remove(c1)
                                alist.append(c1)
                                blist.append(c0)
                            if c1 in bblist:
                                dlog(number, "upping " + str(cflip(c1)) + " and adding %s to alist" % str(cflip(c0)))
                                bblist.remove(c1)
                                blist.append(c1)
                                alist.append(c0)
                        if c1 not in processedlist:
                            processedlist.append(c1)
                            coordtoeval.append(c1)
                            stronglist.append(c1)
                            if c0 in alist:
                                dlog(number, "adding %s to blist" % str(cflip(c1)))
                                blist.append(c1)
                            if c0 in blist:
                                dlog(number, "adding %s to alist" % str(cflip(c1)))
                                alist.append(c1)
                            if c0 in aalist:
                                dlog(number, "upping " + str(cflip(c0)) + " and adding %s to blist" % str(cflip(c1)))
                                aalist.remove(c0)
                                alist.append(c0)
                                blist.append(c1)
                            if c0 in bblist:
                                dlog(number, "upping " + str(cflip(c0)) + " and adding %s to alist" % str(cflip(c1)))
                                bblist.remove(c0)
                                blist.append(c0)
                                alist.append(c1)
                # look for weak links only off strong links
                if coord in stronglist:
                    poss_bin_weak = find_weak_binary_link(pboard, coord, number, x_type)
                    if poss_bin_weak[0]:
                        for c in poss_bin_weak[1]:
                            if c not in alist and c not in blist and c not in aalist and c not in bblist:
                                processedlist.append(c)
                                coordtoeval.append(c)
                                if coord in alist:
                                    dlog(number, "adding %s to bblist" % str(cflip(c)))
                                    bblist.append(c)
                                if coord in blist:
                                    dlog(number, "adding %s to aalist" % str(cflip(c)))
                                    aalist.append(c)
        # since I was able to find at least one binary pair I have the starting of a chain, so return it
        loop = make_a_loop(alist, blist, number)
        if loop[0]:
            return True, [[loop[1], loop[2]]]
        #return True, alist, blist
    # couldnt find shit, return hogwash
    return False, None, None

def make_a_loop(alist, blist, number):
    lists = [alist, blist]
    continue_loop = True
    while continue_loop:
        dlog(number, '-------start loop-------')
        dlog(number, lists)
        continue_loop = False
        for clist in lists:
            for coord in clist:
                seeA = 0
                seeB = 0
                linecds = []
                for x_type in range(3):
                    linecds.extend(get_coord_list(coord, x_type))
                    linecdsset = set(linecds)
                for linecd in linecdsset:
                    if linecd != coord:
                        if linecd in alist:
                            dlog(number, 'A: compared ' + str(linecd) + ' to ' + str(alist))
                            seeA += 1
                        if linecd in blist:
                            dlog(number, 'B: compared ' + str(linecd) + ' to ' + str(blist))
                            seeB += 1
                safe = False
                dlog(number, "checking coord" + str(cflip(coord)))
                if seeA + seeB == 2:
                    dlog(number, "almost safe")
                    if seeA == 2 or seeB == 2:
                        safe = True
                        dlog(number, "safe" + str(seeA) + str(seeB))
                if not safe:
                    dlog(number, "not safe")
                    if coord in alist:
                        alist.remove(coord)
                        continue_loop = True
                        #pass
                    if coord in blist:
                        blist.remove(coord)
                        continue_loop = True
                        #pass
    if len(alist) == len(blist):
        return True, alist, blist
    else:
        return False, [], []


def find_all_simple_chain(pboard, number):
    # find binary state starting point
    binarystart = find_all_binary(pboard, number)
    fullprocessedlist = []
    simple_chains = []
    if binarystart[0]:
        for binarypair in binarystart[1]:
            #log(0, "processing pair "+ str(binarypair))
            #log(0, "full list"+ str(fullprocessedlist))
            # skip processing the pair if its apart of another chain
            if binarypair[0] in fullprocessedlist and binarypair[1] in fullprocessedlist:
                #log(0, "skipping not unique")
                continue
            #log(0, "Its unique! " + str(binarypair))
            coordtoeval = []
            processedlist = []
            alist = []
            blist = []
            first = True
            for c in binarypair:
                coordtoeval.append(c)
                processedlist.append(c)
                if first:
                    first = False
                    alist.append(c)
                else:
                    blist.append(c)
            # pop the position list and mark new binary states adding to the position list
            while len(coordtoeval) > 0:
                coord = coordtoeval.pop()
                for x_type in range(3):
                    poss_bin = find_strong_binary_link(pboard, coord, number, x_type)
                    if poss_bin[0]:
                        c0 = poss_bin[1][0] 
                        c1 = poss_bin[1][1] 
                        # only process the entry not already proccessed and add to alt list
                        if c0 not in processedlist:
                            processedlist.append(c0)
                            coordtoeval.append(c0)
                            if c1 in alist:
                                blist.append(c0)
                            if c1 in blist:
                                alist.append(c0)
                        if c1 not in processedlist:
                            processedlist.append(c1)
                            coordtoeval.append(c1)
                            if c0 in alist:
                                blist.append(c1)
                            if c0 in blist:
                                alist.append(c1)
            # add the chain coords to a full list
            fullprocessedlist += processedlist
            # since I was able to find at least two binary pairs I have the starting of a chain, so add it as a chain
            simple_chains.append([alist, blist])
    if len(simple_chains) > 0:
        # Return my chain
        return True, simple_chains
    else:
        # couldnt find shit, return hogwash
        return False, None, None    
