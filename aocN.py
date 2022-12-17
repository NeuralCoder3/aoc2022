import re
import tqdm
import os
import sys
import collections

file = "aocXX_1.txt"
file = "aocXX.txt"

with open(file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]
