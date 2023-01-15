# advent of code 2019
# day 9

# part 1
intCode = tuple([int(i) for i in open('input.txt', 'r').read().split(',')])

def runProgram(intCode, partTwo=False):
    code = {i: intCode[i] for i in range(len(intCode))}
    c = 0
    inpt = 1 if partTwo is False else 2
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
            code[p1Loc] = inpt
            c += 2
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
            output.append(code[p1Loc])
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

runProgram(intCode)

# part 2
runProgram(intCode, True)