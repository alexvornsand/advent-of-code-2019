# advent of code 2019
# day 7

import itertools

file = 'input.txt'

class Intcode:
    def __init__(self, code): 
        self.script = tuple(code)
        self.program = list(self.script)
        self.pointer = 0
        self.output_value = []
        self.input_value = []
    
    def resetComputer(self):
        self.program = list(self.script)
        self.directive = 'continue'
        self.pointer = 0
        self.output_value = []
        self.input_value = []

    def runProgram(self, input):
        self.directive = 'continue'
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
            self.directive = 'complete'
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
        if len(self.input_value) == 0:
            self.directive = 'pause'
        else:
            self.program[self.identifyValue(parameters[0])] = self.input_value[0]
            self.input_value.pop(0)
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

def part_1(amplifiers):
    amplifierA, amplifierB, amplifierC, amplifierD, amplifierE = amplifiers
    maxThrust = 0
    for permutation in itertools.permutations(list(range(5))):
        amplifierA, amplifierB, amplifierC, amplifierD, amplifierE = amplifiers
        amplifierA.resetComputer()
        amplifierB.resetComputer()
        amplifierC.resetComputer()
        amplifierD.resetComputer()
        amplifierE.resetComputer()
        amplifierA.runProgram([permutation[0], 0])
        amplifierB.runProgram([permutation[1], amplifierA.output_value[0]])
        amplifierC.runProgram([permutation[2], amplifierB.output_value[0]])
        amplifierD.runProgram([permutation[3], amplifierC.output_value[0]])
        amplifierE.runProgram([permutation[4], amplifierD.output_value[0]])
        maxThrust = max(maxThrust, amplifierE.output_value[0])
    maxThrust
    print('Part 1:', maxThrust)

def part_2(amplifiers):
    amplifierA, amplifierB, amplifierC, amplifierD, amplifierE = amplifiers
    maxThrust = 0
    for permutation in itertools.permutations(list(range(5,10))):
        thrust = 0
        amplifierA.resetComputer()
        amplifierB.resetComputer()
        amplifierC.resetComputer()
        amplifierD.resetComputer()
        amplifierE.resetComputer()
        amplifierA.runProgram([permutation[0], thrust])
        thrust = amplifierA.output_value[-1]
        amplifierB.runProgram([permutation[1], thrust])
        thrust = amplifierB.output_value[-1]
        amplifierC.runProgram([permutation[2], thrust])
        thrust = amplifierC.output_value[-1]
        amplifierD.runProgram([permutation[3], thrust])
        thrust = amplifierD.output_value[-1]
        amplifierE.runProgram([permutation[4], thrust])
        thrust = amplifierE.output_value[-1]
        while(amplifierE.directive != 'complete'):
            amplifierA.runProgram([thrust])
            thrust = amplifierA.output_value[-1]
            amplifierB.runProgram([thrust])
            thrust = amplifierB.output_value[-1]
            amplifierC.runProgram([thrust])
            thrust = amplifierC.output_value[-1]
            amplifierD.runProgram([thrust])
            thrust = amplifierD.output_value[-1]
            amplifierE.runProgram([thrust])
            thrust = amplifierE.output_value[-1]
        maxThrust = max(maxThrust, thrust)
    print('Part 2:', maxThrust)

def main():
    code = [int(x) for x in open(file, 'r').read().split(',')]
    amplifiers = [Intcode(code) for i in range(5)]
    part_1(amplifiers)
    part_2(amplifiers)

if __name__ == '__main__':
    main()