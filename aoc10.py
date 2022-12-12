import re

with open("aoc10.txt") as f:
    lines = f.readlines()

# lines = """
# addx 15
# addx -11
# addx 6
# addx -3
# addx 5
# addx -1
# addx -8
# addx 13
# addx 4
# noop
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx -35
# addx 1
# addx 24
# addx -19
# addx 1
# addx 16
# addx -11
# noop
# noop
# addx 21
# addx -15
# noop
# noop
# addx -3
# addx 9
# addx 1
# addx -3
# addx 8
# addx 1
# addx 5
# noop
# noop
# noop
# noop
# noop
# addx -36
# noop
# addx 1
# addx 7
# noop
# noop
# noop
# addx 2
# addx 6
# noop
# noop
# noop
# noop
# noop
# addx 1
# noop
# noop
# addx 7
# addx 1
# noop
# addx -13
# addx 13
# addx 7
# noop
# addx 1
# addx -33
# noop
# noop
# noop
# addx 2
# noop
# noop
# noop
# addx 8
# noop
# addx -1
# addx 2
# addx 1
# noop
# addx 17
# addx -9
# addx 1
# addx 1
# addx -3
# addx 11
# noop
# noop
# addx 1
# noop
# addx 1
# noop
# noop
# addx -13
# addx -19
# addx 1
# addx 3
# addx 26
# addx -30
# addx 12
# addx -1
# addx 3
# addx 1
# noop
# noop
# noop
# addx -9
# addx 18
# addx 1
# addx 2
# noop
# noop
# addx 9
# noop
# noop
# noop
# addx -1
# addx 2
# addx -37
# addx 1
# addx 3
# noop
# addx 15
# addx -21
# addx 22
# addx -6
# addx 1
# noop
# addx 2
# addx 1
# noop
# addx -10
# noop
# noop
# addx 20
# addx 1
# addx 2
# addx 2
# addx -6
# addx -11
# noop
# noop
# noop
# """.strip().split("\n")

# lines = """
# noop
# addx 3
# addx -5
# """.strip().split("\n")

lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]

current_instr = None
cycle = -1
cyclesToComplete=0
X = 1
sum = 0

pos = 0
s=""

while True:
    cycle += 1
    print(cycle, X)
    pos = (cycle-1) % 40
    if X-1 <= pos and X+1 >= pos:
        s += "#"
    else:
        s += "."
    if cycle % 40 == 0:
        s += "\n"
        
    if cycle % 40 == 20:
        sum += X*cycle
    if cyclesToComplete > 0:
        cyclesToComplete -= 1
        if cyclesToComplete > 0:
            continue
    
    if current_instr==None:
        pass
    elif current_instr[0] == "addx":
        X += int(current_instr[1])
    elif current_instr[0] == "noop":
        pass
    print("executed: ", current_instr)
    
    if len(lines) == 0:
        break
    line = lines.pop(0)
    parts = line.split(" ")
    current_instr = parts
    if parts[0] == "addx":
        cyclesToComplete = 2
    elif parts[0] == "noop":
        cyclesToComplete = 1
    print("start executing: ", current_instr)

print("sum: ",sum)
print(s)
