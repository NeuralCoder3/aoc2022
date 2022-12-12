
import sys
import os

strat = []

with open("aoc2.txt") as f:
    lines = f.readlines()

# lines = ["A Y", "B X", "C Z"]

for line in lines:
    line = line.strip()
    if line == "":
        continue
    a, x = line.split(" ")
    a = ord(a[0]) - ord("A")
    x = ord(x[0]) - ord("X")
    strat.append((a, x))

# part 2
prestrat = strat
strat = []
for a, x in prestrat:
    if x == 0:
        strat.append((a, (a+2) % 3))
    elif x == 1:
        strat.append((a, a))
    elif x == 2:
        strat.append((a, (a+1) % 3))

score = 0
for a, x in strat:
    ascore = x+1
    if a == x:
        ascore += 3
    elif x == (a + 1) % 3:
        ascore += 6
    else:
        ascore += 0
    # print(ascore)
    score += ascore

print(score)
