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

distance = []
for i in range(height):
    distance.append([False] * width)
    
for y in range(height):
    for x in range(0,width):
        inc = [(0,1),(1,0),(0,-1),(-1,0)]
        scores = []
        for dx,dy in inc:
            h = lines[y][x]
            i = 1
            d = 0
            while 0 <= y+i*dy < height and 0 <= x+i*dx < width:
                # if lines[y+i*dy][x+i*dx] <= h:
                #     d += 1
                d += 1
                if lines[y+i*dy][x+i*dx] >= h:
                    break
                # h = max(lines[y+i*dy][x+i*dx],h)
                i += 1
            scores.append(d)
        s = 1
        for i in scores:
            s *= i
        distance[y][x] = s
        if x == 0 or x == width-1 or y == 0 or y == height-1:
            distance[y][x] = 0
        print(scores, end=" ")
    print()


count = 0
for y in range(height):
    for x in range(width):
        count = max(count,distance[y][x])
        print(distance[y][x], end=" ")
    print()
print(count)
