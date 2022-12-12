import re

with open("aocN.txt") as f:
    lines = f.readlines()

# lines = """
# """.strip().split("\n")

lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]
