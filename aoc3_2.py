import os

file = "aoc3.txt"

with open(file) as f:
    lines = f.readlines()

# lines = """
# vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw
# """
# lines = lines.strip().split("\n")


lines = [line.strip() for line in lines]

# group lines in groups of 3

groups = []
for i in range(0, len(lines), 3):
    group = []
    for j in range(3):
        group.append(lines[i+j])
    groups.append(group)

sum = 0
for group in groups:
    intersection = set(group[0]) & set(group[1]) & set(group[2])
    char = intersection.pop()
    number = 0
    if char >= "a" and char <= "z":
        number = ord(char) - ord("a") + 1
    elif char >= "A" and char <= "Z":
        number = ord(char) - ord("A") + 1 + 26
    sum += number

print(sum)
