# advent of code 2019
# day 15

# part 1
intCode = [int(x) for x in open('input.txt', 'r').read()[:-1].split(',')]

def navigateMaze(intCode, partTwo=False):
    def evaluatePath(intCode, c, base, path):
        code = intCode.copy()
        output = 1
        while(True):
            paddedC = str(code[c]).zfill(5)
            opcode = int(paddedC[-2:])
            pm1, pm2, pm3 = [int(d) for d in paddedC[:3]][::-1]
            if opcode in [1, 2, 7, 8]: # three-parameter codes
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0
                if pm2 == 0:
                    p2Loc = code[c + 2]
                elif pm2 == 1:
                    p2Loc = c + 2
                else:
                    p2Loc = base + code[c + 2]
                if p2Loc not in code.keys(): code[p2Loc] = 0
                if pm3 == 0:
                    p3Loc = code[c + 3]
                elif pm3 == 1:
                    p3Loc = c + 3
                else:
                    p3Loc = base + code[c + 3]
                if p3Loc not in code.keys(): code[p3Loc] = 0

                # execute code
                if opcode == 1: # addition 
                    code[p3Loc] = code[p1Loc] + code[p2Loc]
                elif opcode == 2: # multiplication 
                    code[p3Loc] = code[p1Loc] * code[p2Loc]
                elif opcode == 7: # less-than 
                    code[p3Loc] = 1 if code[p1Loc] < code[p2Loc] else 0        
                else: # equality 
                    code[p3Loc] = 1 if code[p1Loc] == code[p2Loc] else 0
                c += 4

            elif opcode in [5, 6]: # jump codes
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0
                if pm2 == 0:
                    p2Loc = code[c + 2]
                elif pm2 == 1:
                    p2Loc = c + 2
                else:
                    p2Loc = base + code[c + 2]
                if p2Loc not in code.keys(): code[p2Loc] = 0

                # execute code
                if opcode == 5: # jump if true
                    c = code[p2Loc] if code[p1Loc] != 0 else c + 3
                else: # jump if false
                    c = code[p2Loc] if code[p1Loc] == 0 else c + 3

            elif opcode == 3: # read
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0

                # execute code
                if len(path) > 0:
                    code[p1Loc] = path[0]
                    path.pop(0)
                    c += 2
                else:
                    return(output, code, c, base)

            elif opcode == 4: # write
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0

                # execute code
                output = code[p1Loc]
                c += 2
            elif opcode == 9: # shift base
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0

                # execute code
                base += code[p1Loc]
                c += 2
            else:
                break
        return(output)
    def printMap(mapNodes):
        minY = min([key[0] for key in mapNodes])
        maxY = max([key[0] for key in mapNodes])
        minX = min([key[1] for key in mapNodes])
        maxX = max([key[1] for key in mapNodes])
        image = ''
        for y in range(minY, maxY + 1):
            for x in range(minX, maxX + 1):
                if (y, x) in mapNodes:
                    image += mapNodes[(y, x)]['state']
                else:
                    image += ' '
            image += '\n'
        print(image)
    code = {i: intCode[i] for i in range(len(intCode))}    
    mapNodes = {(0, 0): {
        'path': [], 
        'len': 0, 
        'state': 'S', 
        'visited': False, 
        'intCode': code.copy(), 
        'c': 0, 
        'base': 0, 
        'oxygen': False,
        'timeToO2': 999999}}
    queue = [(0, 0)]
    responseKey = {0: '#', 1: '.', 2: 'o'}
    while(True):
        nextQueue = set()
        for node in queue:
            r, c = node
            for neighbor in [(r - 1, c, 1), (r + 1, c, 2), (r, c - 1, 3), (r, c + 1, 4)]:
                y, x, d = neighbor
                if (y, x) in mapNodes:
                    mapNodes[(y, x)]['len'] = min(mapNodes[node]['len'] + 1, mapNodes[(y, x)]['len'])
                else:
                    neighborIntCode = mapNodes[node]['intCode'].copy()
                    neighborC = mapNodes[node]['c']
                    neighborBase = mapNodes[node]['base']
                    neighborPath = mapNodes[node]['path'].copy() + [d]
                    resultOutput, resultIntCode, resultC, resultBase = evaluatePath(neighborIntCode, neighborC, neighborBase, [d])
                    mapNodes[(y, x)] = {
                        'path': neighborPath,
                        'len': len(neighborPath),
                        'state': responseKey[resultOutput],
                        'visited': False,
                        'intCode': resultIntCode,
                        'c': resultC,
                        'base': resultBase,
                        'oxygen': responseKey[resultOutput] == 'o',
                        'timeToO2': 0
                    }
                    if resultOutput != 0:
                        nextQueue.add((y, x))
            mapNodes[node]['visited'] = True
        if len(nextQueue) > 0:
            queue = nextQueue
        else:
            oxygenSource = [key for key in mapNodes if mapNodes[key]['state'] == 'o'][0]
            if partTwo is False:
                return(mapNodes[oxygenSource]['len'])
            else:
                currentNode = oxygenSource
                queue = [oxygenSource]
                while(True):
                    nextQueue = set()
                    for node in queue:
                        r, c = node
                        for neighbor in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                            y, x = neighbor
                            if (y, x) in mapNodes and mapNodes[(y, x)]['state'] != '#' and mapNodes[(y, x)]['oxygen'] is False:
                                mapNodes[(y, x)]['oxygen'] = True
                                mapNodes[(y, x)]['timeToO2'] = mapNodes[node]['timeToO2'] + 1
                                nextQueue.add((y, x))
                    if len(nextQueue) == 0:
                        return(mapNodes[node]['timeToO2'])
                    else:
                        queue = nextQueue

navigateMaze(intCode)

# part 2
navigateMaze(intCode)