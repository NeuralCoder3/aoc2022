import re


# O(k*n) instead of O(n)
# O(n) would be to keep track of the characters in a bitset/map and the maximum count

with open("aoc6.txt") as f:
    text = f.read()

# text = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
# text = "bvwbjplbgvbhsrlpgdmjqwftvncz"
# text = "nppdvjthqldpwncqszvftbrmjlhg"
# text = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"

# lines = [line.strip() for line in lines]
c = 4
c = 14
window = text[:c]
pos = c
while pos < len(text):
    if len(set(window)) == c:
        print(pos)
        break
    window = window[1:]+text[pos]
    pos += 1
