from functools import lru_cache
import re

file = "aoc19_1.txt"
# file = "aoc19.txt"

with open(file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]

pattern = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")

blueprints = []
for line in lines:
    m = pattern.match(line)
    if not m:
        continue
    blueprint = m.groups()
    num = int(blueprint[0])
    ore_ore = int(blueprint[1])
    clay_ore = int(blueprint[2])
    obsidian_ore = int(blueprint[3])
    obsidian_clay = int(blueprint[4])
    geode_ore = int(blueprint[5])
    geode_obsidian = int(blueprint[6])
    blueprints.append(
        (num, ore_ore, clay_ore, obsidian_ore,
         obsidian_clay, geode_ore, geode_obsidian)
    )

time = 24
for b in blueprints:
    num, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = b

    print(b)

    @lru_cache(maxsize=None)
    def get_geodes(time,
                   oreR=1, clayR=0, obsidianR=0,
                   ore=0, clay=0, obsidian=0):
        if time == 0:
            return 0
        new_ore = ore + oreR
        new_clay = clay + clayR
        new_obsidian = obsidian + obsidianR
        # new_geode = geode + geodeR
        geode = get_geodes(time - 1,
                           oreR, clayR, obsidianR,
                           new_ore, new_clay, new_obsidian)
        if ore_ore <= ore:
            geode = max(
                geode,
                get_geodes(time - 1,
                           oreR + 1, clayR, obsidianR,
                           new_ore - ore_ore, new_clay, new_obsidian)
            )
        if clay_ore <= ore:
            geode = max(
                geode,
                get_geodes(time - 1,
                           oreR, clayR + 1, obsidianR,
                           new_ore - clay_ore, new_clay, new_obsidian)
            )
        if obsidian_ore <= ore and obsidian_clay <= clay:
            geode = max(
                geode,
                get_geodes(time - 1,
                           oreR, clayR, obsidianR + 1,
                           new_ore - obsidian_ore, new_clay - obsidian_clay, new_obsidian)
            )
        if geode_ore <= ore and geode_obsidian <= obsidian:
            geode = max(
                geode,
                get_geodes(time - 1,
                           oreR, clayR, obsidianR,
                           new_ore - geode_ore, new_clay, new_obsidian - geode_obsidian) +
                time-1
            )

        return geode

    print(num, get_geodes(time))
