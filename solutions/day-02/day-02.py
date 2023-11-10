# advent of code 2019
# day 2

file = 'input.txt'

class Intcode:
    def __init__(self, code): 
        self.script = tuple(code)
        self.program = list(self.script)
        self.directive = 'continue'
        self.pointer = 0
    
    def resetComputer(self):
        self.program = list(self.script)
        self.directive = 'continue'
        self.pointer = 0

    def runProgram(self):
        while(self.directive == 'continue'):
            self.evaluateStep()

    def evaluateStep(self):
        code = self.program[self.pointer]
        if code == 1:
            self.add(self.pointer + 1, self.pointer + 2, self.pointer + 3)
            self.directive = 'continue'
            self.pointer += 4
        elif code == 2:
            self.multiply(self.pointer + 1, self.pointer + 2, self.pointer + 3)
            self.directive = 'continue'
            self.pointer += 4
        elif code == 99:
            self.directive = 'break'
            self.pointer += 1
        else:
            self.directive = 'damaged'

    def add(self, addressA, addressB, addressC):
        self.program[self.program[addressC]] = self.program[self.program[addressA]] + self.program[self.program[addressB]]

    def multiply(self, addressA, addressB, addressC):
        self.program[self.program[addressC]] = self.program[self.program[addressA]] * self.program[self.program[addressB]]

def part_1(PROGRAMALERT1202):
    PROGRAMALERT1202.program[1] = 12
    PROGRAMALERT1202.program[2] = 2
    PROGRAMALERT1202.runProgram()
    print('Part 1:', PROGRAMALERT1202.program[0])

def part_2(PROGRAMALERT1202):
    for noun in range(100):
        for verb in range(100):
            PROGRAMALERT1202.resetComputer()
            PROGRAMALERT1202.program[1] = noun
            PROGRAMALERT1202.program[2] = verb
            PROGRAMALERT1202.runProgram()
            if PROGRAMALERT1202.program[0] == 19690720:
                print('Part 2:', str(100 * noun + verb))
                break
            
def main():
    code = [int(x) for x in open(file, 'r').read().split(',')]
    PROGRAMALERT1202 = Intcode(code)
    part_1(PROGRAMALERT1202)
    part_2(PROGRAMALERT1202)

if __name__ == '__main__':
    main()