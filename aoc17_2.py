import re
import tqdm
import os
import sys
import collections

file = "aoc17_1.txt"
# file = "aoc17.txt"

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


meta_block = None
meta_count = len(tiles)
meta_steps = 0


def isOverlapping(tile, x, y, gameboard, cutoff=100):
    overlap = False
    # for i in range(min(len(tile), 10)):
    # for i, row in enumerate(tile):
    for tile_y in range(len(tile)-1, max(len(tile)-cutoff-1, -1), -1):
        # for tile_y in range(len(tile)):
        # tile_y = len(tile)-i-1
        # tile_y = i
        board_y = y-tile_y
        if board_y not in gameboard:
            continue
        row = tile[tile_y]
        for j, c in enumerate(row):
            if c == "#":
                if gameboard[board_y][x+j] == "#":
                    overlap = True
                    break
        if overlap:
            break
    return overlap


def computeBoard(max_count, moves):
    gameboard = collections.defaultdict(lambda: ["."]*w)
    current_tile = 0
    max_y = 0
    x = 2
    y = max_y+3

    steps = 0

    count = 0
    bar = tqdm.tqdm(total=max_count)
    while count < max_count:
        old_x = x
        old_y = y
        # else:
        move = moves[0]
        moves = moves[1:]+moves[0]
        steps += 1
        if current_tile != -1:
            if move == ">":
                x += 1
                if x+len(tiles[current_tile][0]) > w:
                    x -= 1
            elif move == "<":
                x -= 1
                if x < 0:
                    x += 1
        tile = meta_block if current_tile == - \
            1 and meta_block is not None else tiles[current_tile]
        # for i, row in enumerate(tiles[current_tile]):
        # for i in range(max(len(tile),10)):
        #     tile_y = len(tile)-i-1
        #     board_y = y-tile_y
        #     row = tile[tile_y]
        #     for j, c in enumerate(row):
        #         if c == "#":
        #             if gameboard[board_y][x+j] == "#":
        #                 overlap = True
        #                 break
        #     if overlap:
        #         break
        overlap = isOverlapping(tile, x, y, gameboard)
        if overlap:
            x = old_x
        halt = False
        y -= 1
        # check if overlap with bottom
        if y-len(tile)+1 < 0:
            halt = True
        # check if overlap with tiles
        halt = halt or isOverlapping(tile, x, y, gameboard)
        if halt:
            y += 1
            if current_tile == -1:
                x = 0
            max_y = max(max_y, y)
            for i, row in enumerate(tiles[current_tile]):
                if y-i not in gameboard:
                    gameboard[y-i] = ["."]*w
                for j, c in enumerate(row):
                    if c == "#":
                        gameboard[y-i][x+j] = c

            if current_tile == -1:
                skip = meta_steps % len(moves)
                moves = moves[skip:]+moves[:skip]
                steps += meta_steps
                count += meta_count
            else:
                count += 1

            if current_tile == 0 and meta_block is not None and max_count-meta_count > 0:
                current_tile = -1
                tile_height = len(meta_block)
                x = 0
            else:
                current_tile += 1
                current_tile %= len(tiles)
                tile_height = len(tiles[current_tile])
                x = 2
            y = max_y+3+tile_height
            bar.update(1)
        # for py in range(max_y+3, -1, -1):
        #     print("".join(gameboard[py]))
        # print()

    bar.close()

    # print(max_y+1)
    return gameboard, steps, max_y+1


board, steps, max_y = computeBoard(2022, moves)
print(max_y)

board, steps, max_y = computeBoard(meta_count, moves)
meta_block = []
for py in range(max_y, -1, -1):
    meta_block.append("".join(board[py]))

# for py in range(max_y+3, -1, -1):
#     print("".join(board[py]))
# print()
print("\n".join(meta_block))

board, steps, max_y = computeBoard(10, moves)
for py in range(max_y+3, -1, -1):
    print("".join(board[py]))
print()
print(max_y)


# computeGraph(len(tiles)*10)

# while count < 2022:
# max_steps = 1000000000000
# bar = tqdm.tqdm(total=max_steps)
