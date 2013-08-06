
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
# start a master list of all bi-location pairs involved in a chain

# build a list of every bi-location binary pair
# These are all my possible starting points.

# pick the first one.. add it to the master list
# create an alist and a blist format [(number, coord), (number, coord), (number, coord)]
# make an acoord set and a bcoord set for just the coords

# put each number of my starting cell in the alist and the blist and the coords in the acoord set and the bcoord set

# add both of the 2 tuple to a to be processed list

# while loop on the to be proccessed list

# pop the first entry.

# ---bi location check---
# check if the coord of the entry is not in both coord sets
# check if there are only 2 possibilities in the cell
# if so add the cell to the master list
# and add the coord to both the acoord set and the bcoord set
# check and add each 2 tuple to the alist or the blist
# add the new entry to the to be processed list 

# ---bi value check---
# do a bi-value check
#  re-use code from simple chain
#  and add the coord to both the acoord set and the bcoord set

# package all this information into some format
# build the next chain

# return all my chains


# solve for each chain

# for y in range(9)
# for x in range(9)

# # every possibility everywhere must be checked to confirm if it can see the chain if sees both it can be removed
# make set of all seen coords
# remove own coord from set

# if coord can see an acoord and a bcoord check further

# for each possibility in cell
# make a 2 tuple and verify number isnt part of the chain
#  if not
#   for each coord in set
#    if coord in acoordset and in bcoordset
#     make 2 tuples of the number and coord check if tuple in the alist and blist
#     if both are true
#      remove possibility from cell

# # if two bivalue links end up in the same cell a third possibility cant be the solution
# if len(possibilities) > 2 and the coord is both in acoord set and bcoord set
#   for each possibility in cell
#    make a 2 tuple and check if its in alist or in blist
#      if not remove 

# # special case for chain coords
# if coord in acoord set xor bcoord set
#  for num in cell
#    if 2 tuple in alist
#      for other nums 
#        for all seen coords
#          if coord in bcoord set
#           if num in possibility
#            remove 3rd + num 

# for entry in alist and blist
#  if entry can see its same number elsewhere in the xlist
#   the whole xlist is invalid

# if progress was made
#  do all my reporting functions

def find_bi_loc_cells(pboard):
    cells = []
    for y in range(9):
        for x in range(9):
            if len(pboard[y][x]) == 2:
                cells.append((y, x))
    return cells

def bi_loc_check(pboard, tuple_to_check, alist, blist, acoordset, bcoordset):
    coord = tuple_to_check[1]
    y,x = coord[0], coord[1]
    if len(pboard[y][x]) == 2:
        #log(0, "Eval'ing possible bi_loc " + str(coord))
        #log(0, acoordset)
        #log(0, bcoordset)
        # dont bother checking if both numbers are already in the chain
        if bool(coord in acoordset) ^ bool(coord in bcoordset):    
            #log(0, str(coord) + " not in one of the coord sets")
            if tuple_to_check in alist:
                if (pboard[y][x][0], coord) == tuple_to_check:
                    new_tuple = (pboard[y][x][1], coord)
                if (pboard[y][x][1], coord) == tuple_to_check:
                    new_tuple = (pboard[y][x][0], coord)
                blist.append(new_tuple)
                bcoordset.add(coord)
                return new_tuple
            if tuple_to_check in blist:
                if (pboard[y][x][0], coord) == tuple_to_check:
                    new_tuple = (pboard[y][x][1], coord)
                if (pboard[y][x][1], coord) == tuple_to_check:
                    new_tuple = (pboard[y][x][0], coord)
                alist.append(new_tuple)
                acoordset.add(coord)
                return new_tuple
    return False

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


def bi_val_check(pboard, tuple_to_check, alist, blist, acoordset, bcoordset):
    number, coord = tuple_to_check[0], tuple_to_check[1]
    new_tuple_list = []
    for x_type in range(3):
        poss_bin = find_strong_binary_link(pboard, coord, number, x_type)
        if poss_bin[0]:
            for c in poss_bin[1]:
                if (number, c) !=  tuple_to_check:
                    new_tuple = (number, c)
            # verify new tuple isnt already part of the chain
            if new_tuple not in alist and new_tuple not in blist:
                if tuple_to_check in alist:
                    blist.append(new_tuple)
                    bcoordset.add(new_tuple[1])
                if tuple_to_check in blist:
                    alist.append(new_tuple)
                    acoordset.add(new_tuple[1])
                new_tuple_list.append(new_tuple)
    if len(new_tuple_list) > 0:
        return new_tuple_list
    else:
        return False



def find_all_chains(pboard):
    chains = []
    all_bi_loc_cells = find_bi_loc_cells(pboard)
    for coord in all_bi_loc_cells:
        #log(0, "---Starting new chain---")
        y,x = coord[0], coord[1]
        alist = [(pboard[y][x][0], coord)]
        blist = [(pboard[y][x][1], coord)]
        acoordset = set()
        bcoordset = set()
        # I cant init the set with the coord, I have to add it, dunno why
        acoordset.add(coord)
        bcoordset.add(coord)
        chain_coords_to_process = [(pboard[y][x][0], coord), (pboard[y][x][1], coord)]
        while len(chain_coords_to_process) > 0:
            tuple_to_check = chain_coords_to_process.pop()
            # Do a Bi-location(binary choice in the same location) check on the tuple
            potential_bi_loc = bi_loc_check(pboard, tuple_to_check, alist, blist, acoordset, bcoordset)
            if potential_bi_loc:
                chain_coords_to_process.append(potential_bi_loc)
                #If the bi-location coord is part of a chain, it wont make a new unique chain later... remove
                if potential_bi_loc[1] in all_bi_loc_cells:
                    all_bi_loc_cells.remove(potential_bi_loc[1])
            # Do a Bi-Value(binary choice of the number) check on the tuple
            potential_bi_val = bi_val_check(pboard, tuple_to_check, alist, blist, acoordset, bcoordset)
            if potential_bi_val:
                for new_tup in potential_bi_val:
                    chain_coords_to_process.append(new_tup)
        chains.append([alist, blist, acoordset, bcoordset])
    if len(chains) > 0:
        return chains
    else:
        return False

def seen_trim(pboard, self_coord, chain):
    alist, blist, acoordset, bcoordset = chain[0], chain[1], chain[2], chain[3]
    y, x = self_coord[0], self_coord[1]
    excess_trimmed = [] 
    all_coords = set()
    for x_type in range(3):
        coords = get_coord_list(self_coord, x_type)
        for c in coords:
            all_coords.add(c)
    all_coords.remove(self_coord)
    Aseen = set()
    Bseen = set()
    for coord in all_coords:
        if coord in acoordset:
            Aseen.add(coord)
        if coord in bcoordset:
            Bseen.add(coord)
    if Aseen and Bseen:
        for poss_num in pboard[y][x]:
            p_num_seeA = False
            p_num_seeB = False
            for Acoord in Aseen:
                if (poss_num, Acoord) in alist:
                    p_num_seeA = True
                    #log(0, "eval sees A")
            for Bcoord in Bseen:
                if (poss_num, Bcoord) in blist:
                    p_num_seeB = True
                    #log(0, "eval sees B")
            #log(0, p_num_seeA)
            #log(0, p_num_seeB)
            if p_num_seeA and p_num_seeB:
                pboard[y][x].remove(poss_num)
                excess_trimmed.append(poss_num)
                #log(0, "removing " + str(poss_num) + " from " + str(self_coord))
    return excess_trimmed

def both_cell_trim(pboard, self_coord, chain):
    trimmed = []
    if len(pboard[self_coord[0]][self_coord[1]]) > 2:
        alist, blist, acoordset, bcoordset = chain[0], chain[1], chain[2], chain[3]
        if self_coord in acoordset and self_coord in bcoordset:
            for num in pboard[self_coord[0]][self_coord[1]]:
                if (num, self_coord) not in alist and (num, self_coord) not in blist:
                    #log(0, "trimming " + str(num) + " from my cramped cell " + str(self_coord))
                    pboard[self_coord[0]][self_coord[1]].remove(num)
                    trimmed.append(num)
    return trimmed

def half_and_half_trim(pboard, self_coord, chain):
    trimmed = []
    if len(pboard[self_coord[0]][self_coord[1]]) > 2:
        alist, blist, acoordset, bcoordset = chain[0], chain[1], chain[2], chain[3]
        #log(0, "-----Trimming" + str(self_coord) +  "-----")
        #log(0, alist)
        #log(0, blist)
        itsA = False
        itsB = False
        for num in pboard[self_coord[0]][self_coord[1]]:
            if (num, self_coord) in alist:
                itsA = num
            if (num, self_coord) in blist: 
                itsB = num
        # perfect use of xor!
        if bool(itsA) ^ bool(itsB):
            all_coords = set()
            for x_type in range(3):
                coords = get_coord_list(self_coord, x_type)
                for c in coords:
                    all_coords.add(c)
            all_coords.remove(self_coord)
            if itsA:
                #log(0, itsA)
                for item in blist:
                    if item[1] in all_coords and item[0] in pboard[self_coord[0]][self_coord[1]] and item[0] != itsA:
                        pboard[self_coord[0]][self_coord[1]].remove(item[0])
                        #log(0, "blist found removed " + str(item[0]) + " from " + str(cflip(self_coord)))
                        trimmed.append(item[0])
            if itsB:
                #log(0, itsB)
                for item in alist:
                    if item[1] in all_coords and item[0] in pboard[self_coord[0]][self_coord[1]] and item[0] != itsB:
                        pboard[self_coord[0]][self_coord[1]].remove(item[0])
                        #log(0, "alist found removed " + str(item[0]) + " from " + str(cflip(self_coord)))
                        trimmed.append(item[0])
    return trimmed

def trim_cleanup(list_of_trims, chain_display, msg, any_trim, y, x):
    if not any_trim:
        GAMESTEPS[0] += 1
        any_trim = True
    for removed_number in list_of_trims:
        trimme_msg = "trimmed " + str(removed_number) + msg
        onetimelist = chain_display[:]
        onetimelist.append(((y, x), removed_number, 'remove'))
        support.update_gamestepslog('pboard', 'remove', (y, x), removed_number, trimme_msg, False, onetimelist)
    return any_trim


def invalid_xlist(xlist):
    for entry in xlist:
        all_coords = set()
        for x_type in range(3):
            coords = get_coord_list(entry[1], x_type)
            for c in coords:
                all_coords.add(c)
        all_coords.remove(entry[1])
        for coord in all_coords:
            if (entry[0], coord) in xlist:
                return True
    return False




def trim_chain(pboard, chain):
    any_trim = False
    alist, blist, acoordset, bcoordset = chain[0], chain[1], chain[2], chain[3]
    if len(alist) < 2 and len(blist) < 2: 
        return False
    #log(0, "-----chain-----")
    #log(0, alist)
    #log(0, blist)
    chain_display = []
    for item in alist:
        chain_display.append((item[1], item[0], "set1"))
    for item in blist:
        chain_display.append((item[1], item[0], "set2"))
    # I presume this will work just fine, but I dont have an example to test with... so leaving in this state
    if invalid_xlist(alist):
        log(0, "I found an invalid chain its the alist")
        log(0, alist)
    if invalid_xlist(blist):
        log(0, "I found an invalid chain its the blist")
        log(0, blist)
    for y in range(9):
        for x in range(9):
            if len(pboard[y][x]) > 0:
                if (y, x) in acoordset or (y, x) in bcoordset:
                    #log(0, "Processing chain cell")
                    cramped = both_cell_trim(pboard, (y, x), chain)
                    if cramped:
                        msg = " because both chains are in the cell"
                        any_trim = trim_cleanup(cramped, chain_display, msg, any_trim, y, x)
                    half_cramped = half_and_half_trim(pboard, (y, x), chain)
                    if half_cramped:
                        msg = " because its cell has one chain, and it sees the other chain"
                        any_trim = trim_cleanup(half_cramped, chain_display, msg, any_trim, y, x)
                else:
                    #log(0, "Processing non-chain cell " + str((y, x)))
                    excess_seen = seen_trim(pboard, (y, x), chain)
                    if excess_seen:
                        msg = " because its seen by both chains"
                        any_trim = trim_cleanup(excess_seen, chain_display, msg, any_trim, y, x)

    return any_trim

def medusa_chain(board, pboard):
    chains = find_all_chains(pboard)
    if chains:
        for chain in chains:
            trimmed = trim_chain(pboard, chain)
            if trimmed:
                return True
    return False
medusa_chain.name = "Medusa Chain"

