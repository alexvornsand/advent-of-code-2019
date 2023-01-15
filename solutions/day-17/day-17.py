# advent of code 2019
# day 17

# part 1
intCode = [int(x) for x in open('input.txt', 'r').read()[:-1].split(',')]

def navigateScaffolding(intCode, partTwo=False):
    def runProgram(intCode, inpt=[]):
        code = {i: intCode[i] for i in range(len(intCode))}
        c = 0
        base = 0
        output = []
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
                if len(inpt) > 0:
                    code[p1Loc] = inpt[0]
                    inpt.pop(0)
                    c += 2
                else:
                    return(output, intCode.copy(), c, base)

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
                output += [code[p1Loc]]
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
    def decodeMap(mapCode):
        map = ''
        for code in mapCode:
            map += chr(code)
        return([[d for d in line] for line in map.rstrip().splitlines()])
    def analyzeMap(mapGrid):
        intersections = 0
        for r in range(1, len(mapGrid) - 1):
            for c in range(1, len(mapGrid[r]) - 1):
                i = mapGrid[r][c]
                s = mapGrid[r + 1][c]
                n = mapGrid[r - 1][c]
                e = mapGrid[r][c + 1]
                w = mapGrid[r][c - 1]
                if i  == '#' and s == '#' and n == '#' and e == '#' and w == '#':
                    intersections += r * c
        return(intersections)
    def printMap(mapGrid):
        image = ''
        image += '   '
        for c in range(len(mapGrid[0])):
            if c % 5 == 0:
                image += str(c // 10)
            else:
                image += ' '
            image += ' '
        image += '\n'
        image += '   '
        for c in range(len(mapGrid[0])):
            if c % 5 == 0:
                image += str(c % 10)
            else:
                image += ' '
            image += ' '
        image += '\n'
        for r in range(len(mapGrid)):
            if r % 5 == 0:
                image += str(r).zfill(2) + ' '
            else:
                image += '   '
            for c in range(len(mapGrid[r])):
                image += mapGrid[r][c]
                image += ' '
            if r % 5 == 0:
                image += str(r).zfill(2) + ' '
            else:
                image += '   '
            image += '\n'
        image += '   '
        for c in range(len(mapGrid[0])):
            if c % 5 == 0:
                image += str(c // 10)
            else:
                image += ' '
            image += ' '
        image += '\n'
        image += '   '
        for c in range(len(mapGrid[0])):
            if c % 5 == 0:
                image += str(c % 10)
            else:
                image += ' '
            image += ' '
        image += '\n'
        print(image)    
    mapCode = runProgram(intCode.copy())
    mapGrid = decodeMap(mapCode)
    if partTwo is False:
        return(analyzeMap(mapGrid))
    else:
        overrideIntCode = intCode.copy()
        overrideIntCode[0] = 2
        main = 'A,B,A,C,A,B,C,C,A,B'
        A = 'R,8,L,10,R,8'
        B = 'R,12,R,8,L,8,L,12'
        C = 'L,12,L,10,L,8'
        input = [ord(d) for d in main] + [ord('\n')]
        input += eval('[' + (',' + str(ord(',')) + ',').join([','.join([str(ord(x)) for x in a]) for a in A.split(',')]) + ']') + [ord('\n')]
        input += eval('[' + (',' + str(ord(',')) + ',').join([','.join([str(ord(x)) for x in b]) for b in B.split(',')]) + ']') + [ord('\n')]
        input += eval('[' + (',' + str(ord(',')) + ',').join([','.join([str(ord(x)) for x in c]) for c in C.split(',')]) + ']') + [ord('\n')]
        input += [ord('n'), ord('\n')]
        result = runProgram(overrideIntCode, inpt=input)
        return(result[-1])

navigateScaffolding(intCode)

# part 2
navigateScaffolding(intCode, True)