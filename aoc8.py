import re
from math import inf

with open("aoc8.txt") as f:
    lines = f.readlines()

# lines = """
# 30373
# 25512
# 65332
# 33549
# 35390
# """.strip().split("\n")

lines = [line.strip() for line in lines]

height = len(lines)
width = len(lines[0])

visible = []
for i in range(height):
    visible.append([False] * width)
    
# go through each line
for y in range(height):
    prev = -1
    for x in range(0,width):
        if int(lines[y][x]) > prev:
            visible[y][x] = True
        prev = max(prev,int(lines[y][x]))
    prev = -1
    for x in range(width-1,-1,-1):
        if int(lines[y][x]) > prev:
            visible[y][x] = True
        prev = max(prev,int(lines[y][x]))


for x in range(width):
    prev = -1
    for y in range(0,height):
        if int(lines[y][x]) > prev:
            visible[y][x] = True
        prev = max(prev,int(lines[y][x]))
    prev = -1
    for y in range(height-1,-1,-1):
        if int(lines[y][x]) > prev:
            visible[y][x] = True
        prev = max(prev,int(lines[y][x]))

count = 0
for y in range(height):
    for x in range(width):
        if visible[y][x]:
            count += 1
        print(1 if visible[y][x] else 0, end="")
    print()
print(count)
