# advent of code 2019
# day 7

# part 1
import itertools

intCode = tuple([int(x) for x in open('input.txt', 'r').read().split(',')])

def maximizeThrust(intCode, partTwo=False):
    def calcThrust(intCode, amplifiers, partTwo=False):
        if partTwo is False:
            code = list(intCode)
        codes = {
            'a': list(intCode),
            'b': list(intCode),
            'c': list(intCode),
            'd': list(intCode),
            'e': list(intCode),
        }
        cursors = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0,
            'e': 0,        
        }
        phases = {
            'a': amplifiers[0],
            'b': amplifiers[1],
            'c': amplifiers[2],
            'd': amplifiers[3],
            'e': amplifiers[4],
        }
        loop = 0
        ampIds = ['a', 'b', 'c', 'd', 'e'] 
        ampIndex = 0
        amplifier = ampIds[ampIndex]
        i = 0
        inOut = 0
        while(True):
            if partTwo is True:
                code = codes[amplifier]
            phase = phases[amplifier]
            paddedC = str(code[cursors[amplifier]]).zfill(5)
            opcode = int(paddedC[-2:])
            pm1, pm2, pm3 = [int(d) for d in paddedC[:3]][::-1]
            try:
                p1 = code[code[cursors[amplifier] + 1]] if pm1 == 0 else code[cursors[amplifier] + 1]
                p2 = code[code[cursors[amplifier] + 2]] if pm2 == 0 else code[cursors[amplifier] + 2]
            except:
                pass
            if opcode == 99:
                break
            elif opcode == 1:
                code[code[cursors[amplifier] + 3]] = p1 + p2
                cursors[amplifier] += 4
            elif opcode == 2:
                code[code[cursors[amplifier] + 3]] = p1 * p2
                cursors[amplifier] += 4
            elif opcode == 3:
                if loop == 0:
                    if pm1 == 0:
                        code[code[cursors[amplifier] + 1]] = phase if i == 0 else inOut
                    else:
                        code[cursors[amplifier] + 1] = phase if i == 0 else inOut
                    i += 1
                else:
                    if pm1 == 0:
                        code[code[cursors[amplifier] + 1]] = inOut
                    else:
                        code[cursors[amplifier] + 1] = inOut                
                cursors[amplifier] += 2
            elif opcode == 4:
                inOut = p1
                cursors[amplifier] += 2
                ampIndex = (ampIndex + 1) % 5
                amplifier = ampIds[ampIndex]
                if partTwo is False:
                    if amplifier == 'a':
                        break
                    else:
                        i = 0
                else:
                    if amplifier == 'a':
                        loop += 1
                    else:
                        i = 0
            elif opcode == 5:
                if p1 != 0:
                    cursors[amplifier] = p2
                else:
                    cursors[amplifier] += 3
            elif opcode == 6:
                if p1 == 0:
                    cursors[amplifier] = p2
                else:
                    cursors[amplifier] += 3
            elif opcode == 7:
                code[code[cursors[amplifier] + 3]] = 1 if p1 < p2 else 0
                cursors[amplifier] += 4
            elif opcode == 8:
                code[code[cursors[amplifier] + 3]] = 1 if p1 == p2 else 0
                cursors[amplifier] += 4
            else:
                return('BAD CODE!')
        return(inOut)
    if partTwo is False:
        return(max([calcThrust(intCode, p) for p in list(itertools.permutations(list(range(5))))]))
    else:
        return(max([calcThrust(intCode, p, True) for p in list(itertools.permutations(list(range(5, 10))))]))

maximizeThrust(intCode)

# part 2
maximizeThrust(intCode, True)