import re

with open("aoc7.txt") as f:
    lines = f.readlines()

# lines = """
# $ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k
# """.strip().split("\n")

lines = [line.strip() for line in lines]

# map from dir to list of files/dirs
dirs = {
}

current_dir = ""

for line in lines:
    # print(line)
    if line.startswith("$ cd "):
        dir = line[5:]
        if dir == "/":
            current_dir = dir
        elif dir == "..":
            current_dir = current_dir.rsplit("/", 1)[0]
        else:
            current_dir = current_dir + "/" + dir
        current_dir = current_dir.replace("//", "/")

        if current_dir not in dirs:
            dirs[current_dir] = []
    elif line.startswith("$ ls"):
        continue
    else:
        parts = line.split(" ")
        name = " ".join(parts[1:])
        name = current_dir + "/" + name
        name = name.replace("//", "/")
        dirs[current_dir].append((parts[0], name))
        print(current_dir, name, parts[0])

dir_sizes = {}


def get_size(p):
    if p[0] != "dir":
        return int(p[0])
    d = p[1]
    if d in dir_sizes:
        return dir_sizes[d]
    return sum(get_size(p) for p in dirs[d])


s = 0
for p in dirs.keys():
    dir_sizes[p] = get_size(("dir", p))
    if dir_sizes[p] <= 100000:
        print(p, dir_sizes[p])
        s += dir_sizes[p]

print(s)

space = 70000000
rem = space - dir_sizes["/"]
need = 30000000-rem
d = []
for p in dirs.keys():
    if dir_sizes[p] >= need:
        d.append(dir_sizes[p])

print(min(d))
