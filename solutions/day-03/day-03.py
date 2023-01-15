# advent of code 2019
# day 3

# part 1
wires = [wire.split(',') for wire in open('input.txt', 'r').read().split('\n')[:-1]]

def findIntersection(wires, partTwo=False):
    def mapPath(wire):
        x = y = time = 0
        step = {
            'R': (1,0),
            'L': (-1,0),
            'U': (0,1),
            'D': (0,-1)
        }
        path = {(x,y): time}
        for segment in wire:
            for i in range(int(segment[1:])):
                moveX, moveY = step[segment[0]]
                x += moveX
                y += moveY
                time += 1
                path[(x,y)] = time
        return(path)
    wire0Path = mapPath(wires[0])
    wire1Path = mapPath(wires[1])
    overlaps = sorted(list(set(wire0Path.keys()).intersection(wire1Path.keys())), key=lambda c: abs(c[0]) + abs(c[1]))
    if partTwo is False:
        return(abs(overlaps[1][0]) + abs(overlaps[1][1]))
    else:
        return(min([wire0Path[c] + wire1Path[c] for c in overlaps[1:]]))

findIntersection(wires)

# part 2
findIntersection(wires, True)
