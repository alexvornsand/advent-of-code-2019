# advent of code 2019
# day 13

# part 1
intCode = [int(c) for c in open('input.txt', 'r').read()[:-1].split(',')]

def runProgram(intCode, partTwo=False):
    code = {i: intCode[i] for i in range(len(intCode))}
    c = 0
    if partTwo is True:
        code[0] = 2
    base = 0
    output = []
    joystick = 0
    paddle = 0
    ball = 0
    map = {}
    score = 0
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
            code[p1Loc] = joystick
            c += 2

        elif opcode == 4: # write
            # assign parameter values
            if pm1 == 0: 
                p1Loc = code[c + 1]
            elif pm1 == 1:
                p1Loc = c + 1
            else:
                p1Loc = base + code[c + 1]
            if p1Loc not in code.keys(): 
                code[p1Loc] = 0

            # execute code
            if len(output) < 2:
                output.append(code[p1Loc])
            else:
                if output == [-1,0]:
                    score = code[p1Loc]
                elif code[p1Loc] == 3:
                    paddle = output[0]
                    map[tuple(output)] = code[p1Loc]
                elif code[p1Loc] == 4:
                    ball = output[0]
                    map[tuple(output)] = code[p1Loc]
                else:
                    map[tuple(output)] = code[p1Loc]
                output = []
            c += 2
            if paddle < ball:
                joystick = 1
            elif paddle > ball:
                joystick = -1
            else:
                joystick = 0

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
    if partTwo is False:
        return(sum([map[key] == 2 for key in map.keys()]))
    else:
        return(score)

runProgram(intCode)

# part 2
runProgram(intCode, True)