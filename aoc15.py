import re
import tqdm

# voronoi, greedy interval scheduling

# our algorithm for part 2 is not fast but fast enough O(n*k)
# the efficient algorithm is to use a range tree (could be optimized by viewing space rotated by 45°) / modified sweep line algorithm O(k)

lines = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip().split("\n")

with open("aoc15.txt") as f:
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

row = 10
row = 2000000

possibilites = []
# bound = 20
bound = 2*row
for row in tqdm.tqdm(range(0,bound+1)):
    # print(f"Row {row}")

    # covered intervals on row 
    intervals = []
    beacons = set()

    for sx,sy,bx,by,distance in signals:
        dist_on_row = distance - abs(sy - row)
        # print(f"Sensor at {sx},{sy} beacon at {bx},{by} distance {distance} dist_on_row {dist_on_row}")
        int_start = sx - dist_on_row
        int_end = sx + dist_on_row
        if int_start <= int_end:
            intervals.append((int_start,int_end))
        if by == row:
            beacons.add((bx,by))

    count = 0
    pos = None
    intervals.sort()
    # print(intervals)
    for int_start,int_end in intervals:
        if pos is None:
            if int_start > 0:
                possibilites.append((0, int_start-1, row))
            pos = int_start
        else:
            # for i in range(pos, int_start):
            #     print(".", end="")
            # if pos < int_start:
            #     pos = int_start
            # else:
            #     pass
            if pos < int_start:
                possibilites.append((pos, int_start-1, row))
            pos = max(pos, int_start)
        if pos > int_end:
            continue
        count += int_end - pos + 1
        # print(f"Add [{pos},{int_end}] to count, count={count}")
        pos = int_end+1
        # for i in range(pos, int_end):
        #     print("#", end="")
    # print()
    if pos is not None and pos < bound:
        possibilites.append((pos, bound, row))
        
    count -= len(beacons)
    # print(count)
    
print(possibilites)
for start,end,row in possibilites:
    # print(f"Row {row} [{start},{end}]")
    print("Row %d [%d,%d]" % (row,start,end))
