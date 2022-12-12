
# simpler version of scheduling/min-overlap (greedy algorithm)

with open("aoc4.txt") as f:
    lines = f.readlines()

# lines = """
# 2-4,6-8
# 2-3,4-5
# 5-7,7-9
# 2-8,3-7
# 6-6,4-6
# 2-6,4-8
# """.strip().split("\n")

lines = [line.strip() for line in lines]

pairs = []

for line in lines:
    elfs = line.split(",")
    pair0 = ([int(x) for x in elfs[0].split("-")])
    pair1 = ([int(x) for x in elfs[1].split("-")])
    pairs.append((pair0, pair1))


def contained(pair0, pair1):
    return pair0[0] <= pair1[0] and pair0[1] >= pair1[1]


def overlap(pair0, pair1):
    return pair0[0] <= pair1[0] <= pair0[1] or pair0[0] <= pair1[1] <= pair0[1]


sum = 0
overlaped = 0
for pair0, pair1 in pairs:
    if contained(pair0, pair1) or contained(pair1, pair0):
        sum += 1
    if overlap(pair0, pair1) or overlap(pair1, pair0):
        overlaped += 1

print("contained", sum)
print("overlap", overlaped)
