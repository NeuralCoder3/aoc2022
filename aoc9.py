import re

# 2376

with open("aoc9.txt") as f:
    lines = f.readlines()

# lines = """
# R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2
# """.strip().split("\n")

# lines = """
# R 5
# U 8
# L 8
# D 3
# R 17
# D 10
# L 25
# U 20
# """.strip().split("\n")

ntails = 9

lines = [line.strip() for line in lines]
lines = [line for line in lines if line != ""]

# head = (0,0)
# tail = (head[0], head[1])
hx, hy = 0, 0
tails = []
for i in range(ntails+1):
    tails.append((hx, hy))

pos = set()

for l in lines:
    p, n = l.split(" ")
    print(p, n)
    for i in range(int(n)):
        hx,hy = tails[0]
        if p == "R":
            hx,hy = (hx + 1, hy)
        elif p == "L":
            hx,hy = (hx - 1, hy)
        elif p == "U":
            hx,hy = (hx, hy + 1)
        elif p == "D":
            hx,hy = (hx, hy - 1)
        tails[0] = (hx, hy)
            
        for i in range(ntails):
            hx,hy = tails[i]
            tx,ty = tails[i+1]
            dx = abs(hx - tx)
            dy = abs(hy - ty)
            # if dx > 1:
            #     tx += 1 if hx > tx else -1
            # if dy > 1:
            #     ty += 1 if hy > ty else -1
            if dx > 1 or dy > 1:
                # move adjacent in same row/column
                # .....    .....    .....
                # .TH.. -> .T.H. -> ..TH.
                # .....    .....    .....

                # ...    ...    ...
                # .T.    .T.    ...
                # .H. -> ... -> .T.
                # ...    .H.    .H.
                # ...    ...    ...
                    
                if tx == hx:
                    ty += (hy - ty) // 2
                elif ty == hy:
                    tx += (hx - tx) // 2
                    
                # move diagonal to head
                # .....    .....    .....
                # .....    ..H..    ..H..
                # ..H.. -> ..... -> ..T..
                # .T...    .T...    .....
                # .....    .....    .....

                # .....    .....    .....
                # .....    .....    .....
                # ..H.. -> ...H. -> ..TH.
                # .T...    .T...    .....
                # .....    .....    .....
                elif tx < hx and ty < hy:
                    tx += 1
                    ty += 1
                elif tx < hx and ty > hy:
                    tx += 1
                    ty -= 1
                elif tx > hx and ty < hy:
                    tx -= 1
                    ty += 1
                elif tx > hx and ty > hy:
                    tx -= 1
                    ty -= 1
                
            tails[i+1] = (tx, ty)
        tx,ty = tails[-1]
        pos.add((tx,ty))
        
        # w = len("..........................")
        # h=w
        # for y in range(h):
        #     for x in range(w):
        #         is_tail = False
        #         for i in range(ntails+1):
        #             if (x,y) == tails[i]:
        #                 is_tail = True
        #                 break
        #         if is_tail:
        #             print(i, end="")
        #         elif (x,y) in pos:
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        # print()
    
print(len(pos))
