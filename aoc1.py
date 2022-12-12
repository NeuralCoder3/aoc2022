import sys
import os

with open("aoc1.txt") as f:
    lines = f.readlines()

elfes = []
elf = []
for line in lines:
    line = line.strip()
    if line == "":
        elfes.append(elf)
        elf = []
    else:
        elf.append(int(line))

if elf != []:
    elfes.append(elf)

sums = [sum(elf) for elf in elfes]
print(max(sums))
top = sorted(sums, reverse=True)[:3]
print(top, sum(top))
