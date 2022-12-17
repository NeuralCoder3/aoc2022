from itertools import chain, combinations
import re
import tqdm
import os
import sys
import functools

# alternative: bitset dp
# idea: dp, path compression

file = "aoc16.txt"

with open(file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]

pattern = re.compile(
    r"Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([\w, ]+)")

valves = {}
for line in lines:
    m = pattern.match(line)
    if m:
        name = m.group(1)
        flow = int(m.group(2))
        tunnels = m.group(3).split(", ")
        valves[name] = {"flow": flow, "tunnels": tunnels}

for name in valves:
    print(name, valves[name])

flow = {}
can_open = valves.keys()

# memoize => dp


@functools.lru_cache(maxsize=None)
def computeFlow(v, time, opened=()):
    if time <= 0:
        return 0
    flow = 0
    if v not in valves:
        return flow
    if v in opened:
        return flow
    add_flow = valves[v]["flow"] * (time-1)
    for tunnel in valves[v]["tunnels"]:
        flow = max(flow, computeFlow(tunnel, time-1, opened))
        if time >= 2 and add_flow > 0 and v in can_open:
            flow = max(flow, computeFlow(tunnel, time-2,
                       tuple(sorted(opened + (v,)))) + add_flow)
    return flow


mflow = computeFlow("AA", 30)
print(mflow)

# part 2

graph = {}
for a in valves:
    graph[a] = {}
    for b in valves:
        if b in valves[a]["tunnels"]:
            graph[a][b] = 1
        else:
            # no connection = infinite
            graph[a][b] = float("inf")

# Floyd-Warshall
for m in valves:
    for a in valves:
        for b in valves:
            # a to b via m
            graph[a][b] = min(graph[a][b], graph[a][m] + graph[m][b])

# nodes of compressed graph
nodes = [v for v in valves if valves[v]["flow"] > 0]

flow = {}


def computeFlow2(v, current, time, opened=()):
    flow[v] = max(flow.get(v, 0), current)
    for next in nodes:
        if next in opened:
            continue
        if time >= graph[v][next]:
            # move to next and open
            remaining = time - graph[v][next] - 1
            computeFlow2(next, current + valves[next]["flow"] *
                         remaining, remaining, tuple(sorted(opened + (next,))))


def is_disjoint(a, b):
    return set(a).isdisjoint(b)


# part 1
# computeFlow2("AA", 0, 30)
# print(max(flow.values()))
computeFlow2("AA", 0, 26)
double_flow = 0
for human in flow:
    for elephant in flow:
        if not is_disjoint(human, elephant):
            continue
        double_flow = max(double_flow, flow[human] + flow[elephant])
print(double_flow)
