import re
import tqdm
import os
import sys
import collections

# file = "aoc17_1.txt"
file = "aoc17.txt"

with open(file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]

moves = lines[0]

tiles = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".strip().split("\n\n")

tiles = [tile.split("\n") for tile in tiles]

w = 7
gameboard = collections.defaultdict(lambda: ["."]*w)

current_tile = 0
max_y = 0
x = 2
y = max_y+3

count = 0

# memoization of height, tiles, steps
memo_rows = 32
memo = {}
memoized_rows = 0

# while count < 2022:
max_steps = 1000000000000
# max_steps = 2022
steps = 0
bar = tqdm.tqdm(total=max_steps)
while count < max_steps:
    # while count < 10:
    # print(current_tile, x, y)
    move = moves[0]
    moves = moves[1:]+moves[0]
    steps += 1
    old_x = x
    old_y = y
    if move == ">":
        x += 1
        if x+len(tiles[current_tile][0]) > w:
            x -= 1
    elif move == "<":
        x -= 1
        if x < 0:
            x += 1
    overlap = False
    for i, row in enumerate(tiles[current_tile]):
        for j, c in enumerate(row):
            if c == "#":
                if gameboard[y-i][x+j] == "#":
                    overlap = True
                    break
        if overlap:
            break
    if overlap:
        x = old_x
    halt = False
    y -= 1
    # check if overlap with bottom
    if y-len(tiles[current_tile])+1 < 0:
        halt = True
    # check if overlap with tiles
    for i, row in enumerate(tiles[current_tile]):
        for j, c in enumerate(row):
            if c == "#":
                if gameboard[y-i][x+j] == "#":
                    halt = True
                    break
        if halt:
            break
    if halt:
        y += 1
        max_y = max(max_y, y)
        for i, row in enumerate(tiles[current_tile]):
            for j, c in enumerate(row):
                if c == "#":
                    gameboard[y-i][x+j] = c

        current_tile += 1
        current_tile %= len(tiles)
        y = max_y+3+len(tiles[current_tile])
        x = 2
        count += 1
        bar.update(1)

        if max_y > memo_rows:
            hash = []
            for i in range(memo_rows):
                hash.append("".join(gameboard[max_y-i]))
            hash = "".join(hash)
            hash = (current_tile, steps % len(moves), hash)
            # print(hash)

            if hash in memo:
                old_count, old_max_y = memo[hash]
                delta_count = count - old_count
                delta_y = max_y+memoized_rows - old_max_y
                units = (max_steps - count) // delta_count
                memoized_rows += units * delta_y
                count += units * delta_count
                # print("found, units", units, "delta count",
                #       delta_count, "delta y", delta_y)
                bar.update(units)
            else:
                memo[hash] = (count, max_y+memoized_rows)
    # for py in range(max_y+3, -1, -1):
    #     print("".join(gameboard[py]))
    # print()

print(max_y+memoized_rows+1)
