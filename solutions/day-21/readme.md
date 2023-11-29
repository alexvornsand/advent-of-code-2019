### [--- Day 21: Springdroid Adventure](https://adventofcode.com/2019/day/21)

You lift off from Pluto and start flying in the direction of Santa.

While experimenting further with the tractor beam, you accidentally pull an asteroid directly into your ship! It deals significant damage to your hull and causes your ship to begin tumbling violently.

You can send a droid out to investigate, but the tumbling is causing enough [artificial gravity](https://en.wikipedia.org/wiki/Artificial_gravity) that one wrong step could send the droid through a hole in the hull and flying out into space.

The clear choice for this mission is a droid that can **jump** over the holes in the hull - a **springdroid**.

You can use an [Intcode](https://adventofcode.com/2019/day/9) program (your puzzle input) running on an [ASCII-capable](https://adventofcode.com/2019/day/17) computer to [program](https://en.wikipedia.org/wiki/Programmable_read-only_memory) the springdroid. However, springdroids don't run Intcode; instead, they run a simplified assembly language called **springscript**.

While a springdroid is certainly capable of navigating the artificial gravity and giant holes, it has one downside: it can only remember at most **15** springscript instructions.

The springdroid will move forward automatically, constantly thinking about **whether to jump**. The springscript program defines the logic for this decision.

Springscript programs only use **Boolean values**, not numbers or strings. Two registers are available: `T`, the **temporary value** register, and `J`, the **jump** register. If the jump register is **true** at the end of the springscript program, the springdroid will try to jump. Both of these registers start with the value **false**.

Springdroids have a sensor that can detect **whether there is ground** at various distances in the direction it is facing; these values are provided in **read-only registers**. Your springdroid can detect ground at four distances: one tile away (`A`), two tiles away (`B`), three tiles away (`C`), and four tiles away (`D`). If there is ground at the given distance, the register will be true; if there is a hole, the register will be **false**.

There are only three instructions available in springscript:

 - `AND X Y` sets `Y` to **true** if both `X` and `Y` are **true**; otherwise, it sets `Y` to **false**.
 - `OR X Y` sets `Y` to **true** if at least one of `X` or `Y` is **true**; otherwise, it sets `Y` to **false**.
 - `NOT X Y` sets `Y` to **true** if `X` is **false**; otherwise, it sets `Y` to **false**.

In all three instructions, the second argument (`Y`) needs to be a writable register (either `T` or `J`). The first argument (`X`) can be any register (including `A`, `B`, `C`, or `D`).

For example, the one-instruction program `NOT A J` means "if the tile immediately in front of me is not ground, jump".

Or, here is a program that jumps if a three-tile-wide hole (with ground on the other side of the hole) is detected:

```
NOT A J
NOT B T
AND T J
NOT C T
AND T J
AND D J
```

The Intcode program expects ASCII inputs and outputs. It will begin by displaying a prompt; then, input the desired instructions one per line. End each line with a newline (ASCII code `10`). **When you have finished entering your program**, provide the command `WALK` followed by a newline to instruct the springdroid to begin surveying the hull.

If the springdroid **falls into space**, an ASCII rendering of the last moments of its life will be produced. In these, `@` is the springdroid, `#` is hull, and `.` is empty space. For example, suppose you program the springdroid like this:

```
NOT D J
WALK
```

This one-instruction program sets `J` to **true** if and only if there is no ground four tiles away. In other words, it attempts to jump into any hole it finds:

```
.................
.................
@................
#####.###########

.................
.................
.@...............
#####.###########

.................
..@..............
.................
#####.###########

...@.............
.................
.................
#####.###########

.................
....@............
.................
#####.###########

.................
.................
.....@...........
#####.###########

.................
.................
.................
#####@###########
```

However, if the springdroid successfully makes it across, it will use an output instruction to indicate the **amount of damage to the hull** as a single giant integer outside the normal ASCII range.

Program the springdroid with logic that allows it to survey the hull without falling into space. **What amount of hull damage does it report?**

### --- Part 2 ---

There are many areas the springdroid can't reach. You flip through the manual and discover a way to **increase its sensor range**.

Instead of ending your springcode program with `WALK`, use `RUN`. Doing this will enable **extended sensor mode**, capable of sensing ground up to **nine tiles away**. This data is available in **five new read-only registers**:

 - Register `E` indicates whether there is ground **five** tiles away.
 - Register `F` indicates whether there is ground **six** tiles away.
 - Register `G` indicates whether there is ground **seven** tiles away.
 - Register `H` indicates whether there is ground **eight** tiles away.
 - Register `I` indicates whether there is ground **nine** tiles away.

All other functions remain the same.

Successfully survey the rest of the hull by ending your program with `RUN`. **What amount of hull damage does the springdroid now report?**

### [--- Solutions ---](day-21.py)
```Python
# advent of code 2019
# day 21

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

def translateInstructions(instructions):
    return [ord(x) for x in '\n'.join(instructions)]

def part_1(springdroid):
    instructions = [
        'NOT B J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'NOT A T',
        'OR T J',
        'WALK',
        ''        
    ]
    springdroid.resetComputer()
    springdroid.runProgram(translateInstructions(instructions))
    print('Part 1:', springdroid.output_values[-1])

def part_2(springdroid):
    instructions = [
        'NOT B J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'AND H J',
        'NOT A T',
        'OR T J',
        'RUN',
        ''
    ]
    springdroid.resetComputer()
    springdroid.runProgram(translateInstructions(instructions))
    print('Part 2:', springdroid.output_values[-1])

def main():
    code = [int(x) for x in open(file, 'r').read().split(',')]
    springdroid = Intcode(code)
    part_1(springdroid)
    part_2(springdroid)

if __name__ == '__main__':
    main()
```