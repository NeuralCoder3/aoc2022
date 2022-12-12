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

sum = 0
for line in lines:
    if line == "":
        continue
    half = len(line) // 2
    first, second = line[:half], line[half:]
    intersection = set(first) & set(second)
    print(intersection)
    char = intersection.pop()
    number = 0
    if char >= "a" and char <= "z":
        number = ord(char) - ord("a") + 1
    elif char >= "A" and char <= "Z":
        number = ord(char) - ord("A") + 1 + 26
    sum += number

print(sum)
