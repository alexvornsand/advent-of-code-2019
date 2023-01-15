# advent of code 2019
# day 5

# part 1
inputCode = tuple([int(i) for i in open('input.txt', 'r').read().split(',')])

def runProgram(inputCode, partTwo=False):
    code = list(inputCode)
    c = 0
    log = []
    inpt = 5 if partTwo else 1
    while(True):
        paddedC = str(code[c]).zfill(5)
        opcode = int(paddedC[-2:])
        pm1, pm2, pm3 = [int(d) for d in paddedC[:3]][::-1]
        try:
            p1 = code[code[c + 1]] if pm1 == 0 else code[c + 1]
            p2 = code[code[c + 2]] if pm2 == 0 else code[c + 2]
        except:
            pass
        if opcode == 99:
            break
        elif opcode == 1:
            code[code[c + 3]] = p1 + p2
            c += 4
        elif opcode == 2:
            code[code[c + 3]] = p1 * p2
            c += 4
        elif opcode == 3:
            if pm1 == 0:
                code[code[c + 1]] = inpt
            else:
                code[c + 1] = inpt                
            c += 2
        elif opcode == 4:
            log.append(p1)
            c += 2
        elif opcode == 5:
            if p1 != 0:
                c = p2
            else:
                c += 3
        elif opcode == 6:
            if p1 == 0:
                c = p2
            else:
                c += 3
        elif opcode == 7:
            code[code[c + 3]] = 1 if p1 < p2 else 0
            c += 4
        elif opcode == 8:
            code[code[c + 3]] = 1 if p1 == p2 else 0
            c += 4
        else:
            return('BAD CODE!')
    return(log[-1])      

runProgram(inputCode)

# part 2
runProgram(inputCode, True)