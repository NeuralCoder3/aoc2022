import re
import tqdm
import os
import sys
import collections
import math

# file = "aoc18_1.txt"
file = "aoc18.txt"

sys.setrecursionlimit(100000)

with open(file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]

grid = set()

min_x = 10000000
max_x = -10000000
min_y = min_x
max_y = max_x
min_z = min_x
max_z = max_x


for line in lines:
    x, y, z = line.split(",")
    x = int(x)
    y = int(y)
    z = int(z)
    grid.add((x, y, z))
    min_x = min(min_x, x)
    max_x = max(max_x, x)
    min_y = min(min_y, y)
    max_y = max(max_y, y)
    min_z = min(min_z, z)
    max_z = max(max_z, z)

neighbors = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]

sides = 0
for x, y, z in grid:
    for dx, dy, dz in neighbors:
        if (x+dx, y+dy, z+dz) not in grid:
            sides += 1


print(sides)

visited = set()


def floodfill(pos):
    if pos in grid:
        return 1
    if pos in visited:
        return 0
    visited.add(pos)
    x, y, z = pos
    if x < min_x-2 or x > max_x+2 or y < min_y-2 or y > max_y+2 or z < min_z-2 or z > max_z+2:
        return 0
    count = 0
    for dx, dy, dz in neighbors:
        count += floodfill((x+dx, y+dy, z+dz))
    return count


print(floodfill((0, 0, 0)))

# def sign(x):
#     if x == 0:
#         return 0
#     return x/abs(x)


# sides = 0
# for x, y, z in grid:
#     for dx, dy, dz in neighbors:
#         if (x+dx, y+dy, z+dz) in grid:
#             continue

#         # if (x+dx, y+dy, z+dz) not in grid:
#         isInner = False
#         for ox, oy, oz in grid:
#             dir = (ox-x, oy-y, oz-z)
#             dir = (sign(dir[0]), sign(dir[1]), sign(dir[2]))
#             if dir == (dx, dy, dz):
#                 isInner = True
#                 print(dir, (dx, dy, dz))
#                 print("  ", (x, y, z), (ox, oy, oz))
#                 break
#             # norm = math.sqrt(dir[0]**2 + dir[1]**2 + dir[2]**2)
#             # if norm == 0:
#             #     continue
#             # dir = (dir[0]/norm, dir[1]/norm, dir[2]/norm)
#             # if dir == (dx, dy, dz):
#             #     isInner = True
#             #     break
#         if not isInner:
#             sides += 1

# print(sides)
