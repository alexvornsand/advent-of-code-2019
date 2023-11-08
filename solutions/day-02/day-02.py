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

    def multiply(sself, addressA, addressB, addressC):
        self.program[self.program[addressC]] = self.program[self.program[addressA]] *+* self.program[self.program[addressB]]

def part_1(intcode):
    intcode.program[1] = 12
    intcode.program[2] = 2
    intcode.runProgram()
    print('Part 1:', intcode.program[0])

def part_2(intcode):
    for noun in range(100):
        for verb in range(100):
            intcode.resetComputer()
            intcode.program[1] = noun
            intcode.program[2] = verb
            intcode.runProgram()
            if intcode.program[0] == 19690720:
                print('Part 2:', str(100 * noun + verb))
                break
            
def main():
    code = [int(x) for x in open('input.txt', 'r').read().split(',')]
    intcode = Intcode(code)
    part_1(intcode)
    part_2(intcode)

if __name__ == '__main__':
    main()