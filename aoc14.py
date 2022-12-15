import re

with open("aoc14.txt") as f:
    lines = f.readlines()

# lines = """
# 498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
# """.strip().split("\n")

lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]

draw_lines = []
minx = 500
miny = 0
maxx = 0
maxy = 0

start = (500,0)
for line in lines:
    coords = line.split(" -> ")
    # points=";".join(["(%s,%s)" % (x,y) for x,y in [coord.split(",") for coord in coords]])
    # print(f"[{points}];")
    for p1,p2 in zip(coords,coords[1:]):
        p1x,p1y = [int(x) for x in p1.split(",")]
        p2x,p2y = [int(x) for x in p2.split(",")]
        p1 = (p1x,p1y)
        p2 = (p2x,p2y)
        draw_lines.append((p1,p2))
    
exit(0)
    
for p1,p2 in draw_lines:
    minx = min(minx,p1[0],p2[0])
    miny = min(miny,p1[1],p2[1])
    maxx = max(maxx,p1[0],p2[0])
    maxy = max(maxy,p1[1],p2[1])
    
maxx += 1
minx -= 1
maxy += 1
    
minx -= 200
maxx += 200

grid = [["." for x in range(maxx-minx+1+1)] for y in range(maxy-miny+1+3)]

# draw lines in grid
def draw_line(p1,p2):
    p1x,p1y = p1
    p2x,p2y = p2
    if p1y == p2y:
        # horizontal
        for x in range(min(p1x,p2x),max(p1x,p2x)+1):
            grid[p1y-miny][x-minx] = "#"
    elif p1x == p2x:
        # vertical
        for y in range(min(p1y,p2y),max(p1y,p2y)+1):
            grid[y-miny][p1x-minx] = "#"
    else:
        # diagonal
        for x,y in zip(range(min(p1x,p2x),max(p1x,p2x)+1),range(min(p1y,p2y),max(p1y,p2y)+1)):
            grid[y-miny][x-minx] = "#"
            
# Part 2
draw_line((minx,maxy+1),(maxx+1,maxy+1))
            
for p1,p2 in draw_lines:
    draw_line(p1,p2)
    
for y in range(0,len(grid)):
    for x in range(0,len(grid[y])):
        print(grid[y][x],end="")
    print()
print()

# exit(0)

count = 0
while True:
    sandx,sandy = start
    abyss = False
    # let sand fall
    while True:
        if sandy > maxy:
            abyss = True
            break
        idxx = sandx - minx
        idxy = sandy - miny
        if grid[idxy+1][idxx] == ".":
            sandy += 1
            continue
        elif idxx>0 and grid[idxy+1][idxx-1] == ".":
            sandx -= 1
            sandy += 1
            continue
        elif idxx < len(grid[0])-1 and grid[idxy+1][idxx+1] == ".":
            sandx += 1
            sandy += 1
            continue
        else:
            break
    if abyss or grid[idxy][idxx] != ".":
        break
    count += 1
    grid[idxy][idxx] = "o"
    # for y in range(miny,maxy+1):
    #     for x in range(minx,maxx+1):
    #         print(grid[y-miny][x-minx],end="")
    #     print()
    # print()

print("Count:",count)
