# advent of code 2019
# day 2

# part 1
program = tuple([int(x) for x in open('input.txt', 'r').read().split(',')])

def runProgram(program, noun, verb):
    programMemory = list(program)
    programMemory[1] = noun
    programMemory[2] = verb
    i = 0
    while(True):
        if programMemory[i] == 99:
            break
        else:
            if programMemory[i] == 1:
                programMemory[programMemory[i + 3]] = programMemory[programMemory[i + 1]] + programMemory[programMemory[i + 2]]
                i += 4
            elif programMemory[i] == 2:
                programMemory[programMemory[i + 3]] = programMemory[programMemory[i + 1]] * programMemory[programMemory[i + 2]]
                i += 4
            else:
                break
    return(programMemory[0])

def buildComputer(program, partTwo=False):
    if partTwo is False:
        return(runProgram(program, 12, 2))
    else:
        for n in range(100):
            for v in range(100):
                if runProgram(program, n, v) == 19690720:
                    return(100 * n + v)

buildComputer(program)

# part 2
buildComputer(program, True)
