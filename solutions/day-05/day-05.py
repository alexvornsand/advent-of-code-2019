# advent of code 2019
# day 5

file = 'input.txt'

class Intcode:
    def __init__(self, code): 
        self.script = tuple(code)
        self.program = list(self.script)
        self.directive = 'continue'
        self.pointer = 0
        self.output_value = []
        self.input_value = 0
    
    def resetComputer(self):
        self.program = list(self.script)
        self.directive = 'continue'
        self.pointer = 0
        self.output_value = []

    def runProgram(self, input):
        self.input_value = input
        while(self.directive == 'continue'):
            self.evaluateStep()

    def identifyValue(self, parameter):
        address, parameter_code = parameter
        if parameter_code == 0:
            return self.program[address]
        elif parameter_code == 1:
            return address

    def evaluateStep(self):
        instruction = str(self.program[self.pointer]).zfill(5)
        opcode = int(instruction[-2:])
        parameter_codes = [int(param) for param in instruction[:-2][::-1]]
        if opcode == 1:
            parameters = list(zip([self.pointer + 1, self.pointer + 2, self.pointer + 3], parameter_codes))
            self.add(parameters)
        elif opcode == 2:
            parameters = list(zip([self.pointer + 1, self.pointer + 2, self.pointer + 3], parameter_codes))
            self.multiply(parameters)
        elif opcode == 3:
            parameters = list(zip([self.pointer + 1], parameter_codes))
            self.input(parameters)
        elif opcode == 4:
            parameters = list(zip([self.pointer + 1], parameter_codes))
            self.output(parameters)
        elif opcode == 5:
            parameters = list(zip([self.pointer + 1, self.pointer + 2], parameter_codes))
            self.jumpIfTrue(parameters)
        elif opcode == 6:
            parameters = list(zip([self.pointer + 1, self.pointer + 2], parameter_codes))
            self.jumpIfFalse(parameters)
        elif opcode == 7:
            parameters = list(zip([self.pointer + 1, self.pointer + 2, self.pointer + 3], parameter_codes))
            self.lessThan(parameters)
        elif opcode == 8:
            parameters = list(zip([self.pointer + 1, self.pointer + 2, self.pointer + 3], parameter_codes))
            self.equals(parameters)

        elif opcode == 99:
            self.directive = 'break'
            self.pointer += 1
        else:
            self.directive = 'damaged'

    def add(self, parameters):
        self.program[self.identifyValue(parameters[2])] = self.program[self.identifyValue(parameters[0])] + self.program[self.identifyValue(parameters[1])]
        self.directive = 'continue'
        self.pointer += 4

    def multiply(self, parameters):
        self.program[self.identifyValue(parameters[2])] = self.program[self.identifyValue(parameters[0])] * self.program[self.identifyValue(parameters[1])]
        self.directive = 'continue'
        self.pointer += 4

    def input(self, parameters):
        self.program[self.identifyValue(parameters[0])] = self.input_value
        self.directive = 'continue'
        self.pointer += 2

    def output(self, parameters):
        self.output_value.append(self.program[self.identifyValue(parameters[0])])
        self.directive = 'continue'
        self.pointer += 2

    def jumpIfTrue(self, parameters):
        if self.program[self.identifyValue(parameters[0])] != 0:
            self.directive = 'continue'
            self.pointer = self.program[self.identifyValue(parameters[1])]
        else:
            self.directive = 'continue'
            self.pointer += 3

    def jumpIfFalse(self, parameters):
        if self.program[self.identifyValue(parameters[0])] == 0:
            self.directive = 'continue'
            self.pointer = self.program[self.identifyValue(parameters[1])]
        else:
            self.directive = 'continue'
            self.pointer += 3

    def lessThan(self, parameters):
        if self.program[self.identifyValue(parameters[0])] < self.program[self.identifyValue(parameters[1])]:
            self.directive = 'continue'
            self.program[self.identifyValue(parameters[2])] = 1
        else:
            self.directive = 'continue'
            self.program[self.identifyValue(parameters[2])] = 0
        self.pointer += 4

    def equals(self, parameters):
        if self.program[self.identifyValue(parameters[0])] == self.program[self.identifyValue(parameters[1])]:
            self.directive = 'continue'
            self.program[self.identifyValue(parameters[2])] = 1
        else:
            self.directive = 'continue'
            self.program[self.identifyValue(parameters[2])] = 0
        self.pointer += 4

def part_1(TEST):
    TEST.resetComputer()
    TEST.runProgram(1)
    print('Part 1:', TEST.output_value[-1])

def part_2(TEST):
    TEST.resetComputer()
    TEST.runProgram(5)
    print('Part 2:', TEST.output_value[0])

def main():
    code = [int(x) for x in open(file, 'r').read().split(',')]
    TEST = Intcode(code)
    part_1(TEST)
    part_2(TEST)

if __name__ == '__main__':
    main()