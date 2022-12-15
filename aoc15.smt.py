import re

# file = "aoc15_1.txt"
# bound = 20
file = "aoc15.txt"
bound = 4000000

with open(file) as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]

signals = []
pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
for line in lines:
    m = pattern.match(line)
    if not m:
        print("ERROR")
    sx,sy,bx,by = [int(x) for x in m.groups()]
    distance = abs(sx-bx) + abs(sy-by)
    signals.append((sx,sy,bx,by,distance))

from z3 import *

x,y=Ints('x y')

s = Solver()

s.add(x >= 0)
s.add(y >= 0)
s.add(x <= bound)
s.add(y <= bound)

def abs(x):
    return If(x >= 0,x,-x)

def dist(p1,p2):
  (x1,y1) = p1
  (x2,y2) = p2
  return abs(x1-x2) + abs(y1-y2)

for sx,sy,bx,by,distance in signals:
  s.add(dist((x,y),(sx,sy)) > dist((sx,sy),(bx,by)))
    
if s.check() == sat:
  m=s.model()
  ix = m[x].as_long()
  iy = m[y].as_long()
  print(ix,iy,ix*bound+iy)
  
else:
  print("unsat")
