import re
import sys

sys.setrecursionlimit(10000)

# Alternative: Use Dijkstra's algorithm

with open("aoc12.txt") as f:
    lines = f.readlines()

# lines = """
# Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi
# """.strip().split("\n")

lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]

arr = []
steps = []
sx,sy = 0,0
ex,ey = 0,0
for line in lines:
  row = []
  step_row = []
  for c in line:
    if c == "S":
      sx,sy = len(arr),len(row)
      c = "a"
    elif c == "E":
      ex,ey = len(arr),len(row)
      c = "z"
    row.append(ord(c)-ord("a"))
    step_row.append(None)
    
  arr.append(row)
  steps.append(step_row)
  
# steps[sx][sy] = 0
def fill(x,y,step_count, last_elevation):
  if x < 0 or y < 0 or x >= len(steps) or y >= len(steps[0]):
    return
  if arr[x][y] > last_elevation+1:
    return
  if steps[x][y] != None and steps[x][y] <= step_count:
    return
  steps[x][y] = step_count
  elevation = arr[x][y]
  fill(x+1,y,step_count+1,elevation)
  fill(x-1,y,step_count+1,elevation)
  fill(x,y+1,step_count+1,elevation)
  fill(x,y-1,step_count+1,elevation)

for y in range(len(arr[0])):
  for x in range(len(arr)):
    if arr[x][y] == 0:
      fill(x,y,0,0)
    # print(chr(e+ord("a")),end="")
# fill(sx,sy,0,0)

print(steps[ex][ey])
