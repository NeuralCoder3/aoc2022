import re
from functools import cmp_to_key


# for part 2: instead of sorting in O(n log n) time, we can just count the smaller elements in O(n) time

with open("aoc13.txt") as f:
    lines = f.readlines()

# lines = """
# [1,1,3,1,1]
# [1,1,5,1,1]

# [[1],[2,3,4]]
# [[1],4]

# [9]
# [[8,7,6]]

# [[4,4],4,4]
# [[4,4],4,4,4]

# [7,7,7,7]
# [7,7,7]

# []
# [3]

# [[[]]]
# [[]]

# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [1,[2,[3,[4,[5,6,0]]]],8,9]
# """.strip().split("\n")

lines = [line.strip() for line in lines]

ORDERED = -1
UNORDERED = 1
UNDECIDED = 0

# ordered multiset compare
def compare(line1,line2):
    if isinstance(line1,int):
        if isinstance(line2,int):
            # print("a",line1,line2)
            if line1 < line2:
                return ORDERED
            elif line1 > line2:
                return UNORDERED
            else:
                return UNDECIDED
        else:
            return compare([line1],line2)
    else:
        if isinstance(line2,int):
            return compare(line1,[line2])
        else:
            pass
    # list,list
    min_len = min(len(line1),len(line2))
    for i in range(min_len):
        # print("c",i,line1[i],line2[i])
        comp = compare(line1[i],line2[i])
        if comp != UNDECIDED:
            # print("d",i,comp)
            return comp
    if len(line1) < len(line2):
        return ORDERED
    elif len(line1) > len(line2):
        return UNORDERED
    else:
        return UNDECIDED
        
pair_index = 0
s = 0
packets = []
for i in range(0,len(lines),3):
    pair_index += 1
    line1 = eval(lines[i])
    line2 = eval(lines[i+1])
    packets.append(line1)
    packets.append(line2)
    # print(i,line1,line2)
    comp = compare(line1,line2)
    assert(comp != UNDECIDED)
    if comp == ORDERED:
        s+=pair_index
        print(pair_index)
print(f"sum = {s}")


divider = [[[2]],[[6]]]
for d in divider:
    packets.append(d)
    
# packets.sort(lambda x,y: 1 if compare(x,y) == ORDERED else (-1 if compare(x,y) == UNORDERED else 0))
packets = sorted(packets,key=cmp_to_key(compare))
keys = []
for d in divider:
    keys.append(packets.index(d)+1)
prod = 1
for key in keys:
    prod *= key
print(prod)

