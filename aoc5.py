import re

# simpler version of hanoi
# parsing: parse in 4-char blocks as long as possible regroup/extend+transpose

with open("aoc5.txt") as f:
    lines = f.readlines()

stacks = [
    "PGRN",
    "CDGFLBTJ",
    "VSM",
    "PZCRSL",
    "QDWCVLSP",
    "SMDWNTC",
    "PWGDH",
    "VMCSHPLZ",
    "ZGWLFPR"
]

# lines = """
#     [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3

# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2
# """.strip().split("\n")

# stacks = [
#     "NZ",
#     "DCM",
#     "P"
# ]

lines = [line.strip() for line in lines]
stacks = [list(s) for s in stacks]

while lines[0] != "":
    lines = lines[1:]

regex = re.compile(r"move (\d+) from (\d+) to (\d+)")
for line in lines:
    match = regex.match(line)
    if match:
        disk = int(match.group(1))
        from_stack = int(match.group(2))-1
        to_stack = int(match.group(3))-1
        disks = stacks[from_stack][:disk]
        stacks[from_stack] = stacks[from_stack][disk:]
        # stacks[to_stack] = list(reversed(disks))+stacks[to_stack]
        stacks[to_stack] = list((disks))+stacks[to_stack]

answer = ""
for s in stacks:
    print(s)
    answer += s[0]

print(answer)
