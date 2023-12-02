### [--- Day 25: Cryostasis ---](https://adventofcode.com/2019/day/25)

As you approach Santa's ship, your sensors report two important details:

First, that you might be too late: the internal temperature is `-40` degrees.

Second, that one faint life signature is somewhere on the ship.

The airlock door is locked with a code; your best option is to send in a small droid to investigate the situation. You attach your ship to Santa's, break a small hole in the hull, and let the droid run in before you seal it up again. Before your ship starts freezing, you detach your ship and set it to automatically stay within range of Santa's ship.

This droid can follow basic instructions and report on its surroundings; you can communicate with it through an [Intcode](https://adventofcode.com/2019/day/9) program (your puzzle input) running on an [ASCII-capable](https://adventofcode.com/2019/day/17) computer.

As the droid moves through its environment, it will describe what it encounters. When it says `Command?`, you can give it a single instruction terminated with a newline (ASCII code `10`). Possible instructions are:

- **Movement** via `north`, `south`, `east`, or `west`.
- To **take** an item the droid sees in the environment, use the command `take <name of item>`. For example, if the droid reports seeing a `red ball`, you can pick it up with `take red ball`.
- To **drop** an item the droid is carrying, use the command `drop <name of item>`. For example, if the droid is carrying a `green ball`, you can drop it with `drop green ball`.
- To get a **list of all of the items** the droid is currently carrying, use the command `inv` (for "inventory").
Extra spaces or other characters aren't allowed - instructions must be provided precisely.

Santa's ship is a **Reindeer-class starship**; these ships use pressure-sensitive floors to determine the identity of droids and crew members. The standard configuration for these starships is for all droids to weigh exactly the same amount to make them easier to detect. If you need to get past such a sensor, you might be able to reach the correct weight by carrying items from the environment.

Look around the ship and see if you can find the **password for the main airlock**.

### [--- Solution ---](day-25.py)

```Python
# advent of code 2019
# day 25

from itertools import combinations

file = 'input.txt'

class Intcode:
    def __init__(self, code): 
        self.script = tuple(code)
        self.program = {i: self.script[i] for i in range(len(self.script))}
        self.directive = 'continue'
        self.pointer = 0
        self.relative_base = 0
        self.output_values = []
        self.input_values = []
        self.verbose = False
    
    def clearOutputs(self):
        self.output_values = []
    
    def resetComputer(self):
        self.program = {i: self.script[i] for i in range(len(self.script))}
        self.directive = 'continue'
        self.pointer = 0
        self.relative_base = 0
        self.output_values = []
        self.input_values = []
        self.verbose = False
    
    def clearOutput(self):
        self.output_values = []

    def printProgram(self):
        return [str(key) + ': ' + str(self.program[key]) for key in sorted(list(self.program.keys()))]

    def runProgram(self, input=[]):
        self.directive = 'continue'
        self.input_values = input
        while(self.directive == 'continue'):
            self.evaluateStep()

    def identifyValue(self, parameter):
        address, parameter_code = parameter
        if parameter_code == 0:
            if self.program[address] not in self.program:
                self.program[self.program[address]] = 0
            return self.program[address]
        elif parameter_code == 1:
            if address not in self.program:
                address
            return address
        elif parameter_code == 2:
            if self.relative_base + self.program[address] not in self.program:
                self.program[self.relative_base + self.program[address]] = 0
            return self.relative_base + self.program[address]

    def evaluateStep(self):
        instruction = str(self.program[self.pointer]).zfill(5)
        opcode = int(instruction[-2:])
        parameter_codes = [int(param) for param in instruction[:-2][::-1]]
        if self.verbose:
            print('pointer:', self.pointer)
            print('instruction:', str(self.program[self.pointer]))
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
        elif opcode == 9:
            parameters = list(zip([self.pointer + 1], parameter_codes))
            self.adjustRelativeBase(parameters)
        elif opcode == 99:
            self.directive = 'complete'
            self.pointer += 1
        else:
            self.directive = 'damaged'

    def add(self, parameters):
        if self.verbose:
            print('\tadd:')
            print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), str(self.program[self.pointer + 3]), '...', sep=', ')
            print('\t', str(parameters[2]), ' = ', str(parameters[0]), ' + ', str(parameters[1]), sep='')
            print('\t[', str(self.identifyValue(parameters[2])), '] = ', str(self.program[self.identifyValue(parameters[0])]), ' + ', str(self.program[self.identifyValue(parameters[1])]), sep='')
        self.program[self.identifyValue(parameters[2])] = self.program[self.identifyValue(parameters[0])] + self.program[self.identifyValue(parameters[1])]
        if self.verbose:
            print('\t[', str(self.identifyValue(parameters[2])), '] = ', str(self.program[self.identifyValue(parameters[2])]), sep='')
        self.directive = 'continue'
        self.pointer += 4

    def multiply(self, parameters):
        if self.verbose:
            print('\tmultiply:')
            print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), str(self.program[self.pointer + 3]), '...', sep=', ')
            print('\t', str(parameters[2]), ' = ', str(parameters[0]), ' * ', str(parameters[1]), sep='')
            print('\t[', str(self.identifyValue(parameters[2])), '] = ', str(self.program[self.identifyValue(parameters[0])]), ' * ', str(self.program[self.identifyValue(parameters[1])]), sep='')
        self.program[self.identifyValue(parameters[2])] = self.program[self.identifyValue(parameters[0])] * self.program[self.identifyValue(parameters[1])]
        if self.verbose:
            print('\t[', str(self.identifyValue(parameters[2])), '] = ', str(self.program[self.identifyValue(parameters[2])]), sep='')
        self.directive = 'continue'
        self.pointer += 4

    def input(self, parameters):
        if len(self.input_values) == 0:
            if self.verbose:
                print('\tinput:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), '...', sep=', ')
                print('\tno input')
            self.directive = 'pause'
        else:
            if self.verbose:
                print('\tinput:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), '...', sep=', ')
                print('\t', str(parameters[0]), ' = ', str(self.input_values[0]), sep='')
                print('\t[', str(self.identifyValue(parameters[0])), '] = ', str(self.input_values[0]), sep='')
            self.program[self.identifyValue(parameters[0])] = self.input_values[0]
            if self.verbose:
                print('\t[', str(self.identifyValue(parameters[0])), '] = ', str(self.program[self.identifyValue(parameters[0])]), sep='')
            self.input_values.pop(0)
            self.directive = 'continue'
            self.pointer += 2

    def output(self, parameters):
        if self.verbose:
            print('\toutput:')
            print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), '...', sep=', ')
            print('\t', str(self.program[self.identifyValue(parameters[0])]), sep='')
        self.output_values.append(self.program[self.identifyValue(parameters[0])])
        if self.verbose:
            print('\toutputs:', self.output_values)
        self.directive = 'continue'
        self.pointer += 2

    def jumpIfTrue(self, parameters):
        if self.program[self.identifyValue(parameters[0])] != 0:
            if self.verbose:
                print('\tjump if true:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), '...', sep=', ')
                print('\t', str(self.program[self.identifyValue(parameters[0])]), ' != 0', sep='')
                print('\t\tpointer =', str(self.program[self.identifyValue(parameters[1])]))
            self.directive = 'continue'
            self.pointer = self.program[self.identifyValue(parameters[1])]
            if self.verbose:
                print('\tpointer:', str(self.pointer))
        else:
            if self.verbose:
                print('\tjump if true:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), '...', sep=', ')
                print('\t', str(self.program[self.identifyValue(parameters[0])]), ' != 0', sep='')
                print('\t\tpointer =', str(self.pointer + 3))
            self.directive = 'continue'
            self.pointer += 3
            if self.verbose:
                print('\tpointer:', str(self.pointer))

    def jumpIfFalse(self, parameters):
        if self.program[self.identifyValue(parameters[0])] == 0:
            if self.verbose:
                print('\tjump if false:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), '...', sep=', ')
                print('\t', str(self.program[self.identifyValue(parameters[0])]), ' == 0', sep='')
                print('\t\tpointer ->', str(self.program[self.identifyValue(parameters[1])]))
            self.directive = 'continue'
            self.pointer = self.program[self.identifyValue(parameters[1])]
            if self.verbose:
                print('\tpointer:', str(self.pointer))
        else:
            if self.verbose:
                print('\tjump if false:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), '...', sep=', ')
                print('\t', str(self.program[self.identifyValue(parameters[0])]), ' == 0', sep='')
                print('\t\tpointer ->', self.pointer)
            self.directive = 'continue'
            self.pointer += 3
            if self.verbose:
                print('\tpointer:', str(self.pointer))

    def lessThan(self, parameters):
        if self.program[self.identifyValue(parameters[0])] < self.program[self.identifyValue(parameters[1])]:
            if self.verbose:
                print('\tless than:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), str(self.program[self.pointer + 3]), '...', sep=', ')
                print('\t', str(self.program[self.identifyValue(parameters[0])]), ' < ', str(self.program[self.identifyValue(parameters[1])]), sep='')
                print('\t\t[', str(self.identifyValue(parameters[2])), '] = 1', sep='')
            self.directive = 'continue'
            self.program[self.identifyValue(parameters[2])] = 1
            if self.verbose:
                print('\t[', str(self.identifyValue(parameters[2])), '] = ', str(self.program[self.identifyValue(parameters[2])]), sep='')
        else:
            if self.verbose:
                print('\tless than:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), str(self.program[self.pointer + 3]), '...', sep=', ')
                print('\t', str(self.program[self.identifyValue(parameters[0])]), ' < ', str(self.program[self.identifyValue(parameters[1])]), sep='')
                print('\t\t[', str(self.identifyValue(parameters[2])), '] = 0', sep='')
            self.directive = 'continue'
            self.program[self.identifyValue(parameters[2])] = 0
            if self.verbose:
                print('\t[', str(self.identifyValue(parameters[2])), '] = ', str(self.program[self.identifyValue(parameters[2])]), sep='')
        self.pointer += 4

    def equals(self, parameters):
        if self.program[self.identifyValue(parameters[0])] == self.program[self.identifyValue(parameters[1])]:
            if self.verbose:
                print('\tequal:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), str(self.program[self.pointer + 3]), '...', sep=', ')
                print('\t', str(self.program[self.identifyValue(parameters[0])]), ' == ', str(self.program[self.identifyValue(parameters[1])]), sep='')
                print('\t\t[', str(self.identifyValue(parameters[2])), '] = 1', sep='')
            self.directive = 'continue'
            self.program[self.identifyValue(parameters[2])] = 1
            if self.verbose:
                print('\t[', str(self.identifyValue(parameters[2])), '] = ', str(self.program[self.identifyValue(parameters[2])]), sep='')
        else:
            if self.verbose:
                print('\tequal:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), str(self.program[self.pointer + 2]), str(self.program[self.pointer + 3]), '...', sep=', ')
                print('\t', str(self.program[self.identifyValue(parameters[0])]), ' == ', str(self.program[self.identifyValue(parameters[1])]), sep='')
                print('\t\t[', str(self.identifyValue(parameters[2])), '] = 0', sep='')
            self.directive = 'continue'
            self.program[self.identifyValue(parameters[2])] = 0
            if self.verbose:
                print('\t[', str(self.identifyValue(parameters[2])), '] = ', str(self.program[self.identifyValue(parameters[2])]), sep='')
        self.pointer += 4

    def adjustRelativeBase(self, parameters):
        if self.verbose:
            print('\tadjust relative base:')
            print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), '...', sep=', ')
            print('\t', str(self.relative_base), ' + ', str(self.program[self.identifyValue(parameters[0])]), sep='')
        self.relative_base += self.program[self.identifyValue(parameters[0])]
        if self.verbose:
            print('\trelative base:', str(self.relative_base))
        self.pointer += 2

def part_1(password):
    def inpt(cmd):
        password.clearOutput()
        password.runProgram([ord(x) for x in cmd + '\n'])
    instructions = [
        'west',
        'south',
        'take pointer',
        'south',
        'take prime number',
        'west',
        'take coin',
        'east',
        'north',
        'north',
        'east',
        'south',
        'take festive hat',
        'north',
        'east',
        'south',
        'south',
        'take space heater',
        'south',
        'take astrolabe',
        'north',
        'north',
        'north',
        'north',
        'take wreath',
        'north',
        'west',
        'take dehydrated water',
        'north',
        'east'
    ]    
    password.resetComputer()
    password.runProgram()
    for instruction in instructions:
        inpt(instruction)
    items = ['pointer', 'prime number', 'coin', 'festive hat', 'space heater', 'astrolabe', 'wreath', 'dehydrated water']
    for item in items:
        inpt('drop ' + item)

    for combination in sum([list(map(list, combinations(items, i))) for i in range(len(items) + 1)], []):
        for item in combination:
            inpt('take ' + item)
        inpt('south')
        if 'eject' not in ''.join([chr(x) for x in password.output_values]):
            print('Part 1:', ''.join([chr(x) for x in password.output_values]), sep='\n')
            break
        for item in combination:
            inpt('drop ' + item)

def main():
    code = [int(x) for x in open(file, 'r').read().split(',')]
    password = Intcode(code)
    part_1(password)

if __name__ == '__main__':
    main()
```