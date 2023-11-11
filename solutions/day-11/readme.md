### [--- Day 11: Space Police ---](https://adventofcode.com/2019/day/11)

On the way to Jupiter, you're [pulled over](https://www.youtube.com/watch?v=KwY28rpyKDE) by the **Space Police**.

"Attention, unmarked spacecraft! You are in violation of Space Law! All spacecraft must have a clearly visible **registration identifier**! You have 24 hours to comply or be sent to [Space Jail](https://www.youtube.com/watch?v=BVn1oQL9sWg&t=5)!"

Not wanting to be sent to Space Jail, you radio back to the Elves on Earth for help. Although it takes almost three hours for their reply signal to reach you, they send instructions for how to power up the **emergency hull painting robot** and even provide a small [Intcode program](https://adventofcode.com/2019/day/9) (your puzzle input) that will cause it to paint your ship appropriately.

There's just one problem: you don't have an emergency hull painting robot.

You'll need to build a new emergency hull painting robot. The robot needs to be able to move around on the grid of square panels on the side of your ship, detect the color of its current panel, and paint its current panel **black** or **white**. (All of the panels are currently **black**.)

The Intcode program will serve as the brain of the robot. The program uses input instructions to access the robot's camera: provide `0` if the robot is over a black panel or `1` if the robot is over a white panel. Then, the program will output two values:

- First, it will output a value indicating the **color to paint the panel** the robot is over: `0` means to paint the panel black, and `1` means to paint the panel **white**.
- Second, it will output a value indicating the **direction the robot should turn**: `0` means it should turn **left 90 degrees**, and `1` means it should turn **right 90 degrees**.

After the robot turns, it should always move **forward exactly one panel**. The robot starts facing **up**.

The robot will continue running for a while like this and halt when it is finished drawing. Do not restart the Intcode computer inside the robot during this process.

For example, suppose the robot is about to start running. Drawing black panels as `.`, white panels as `#`, and the robot pointing the direction it is facing (`< ^ > v`), the initial state and region near the robot looks like this:

```.....
.....
..^..
.....
.....
```

The panel under the robot (not visible here because a `^` is shown instead) is also black, and so any input instructions at this point should be provided `0`. Suppose the robot eventually outputs `1` (paint white) and then `0` (turn left). After taking these actions and moving forward one panel, the region now looks like this:

```.....
.....
.<#..
.....
.....
```

Input instructions should still be provided `0`. Next, the robot might output `0` (paint black) and then `0` (turn left):

```.....
.....
..#..
.v...
.....
```

After more outputs (`1,0`, `1,0`):

```.....
.....
..^..
.##..
.....
```

The robot is now back where it started, but because it is now on a white panel, input instructions should be provided `1`. After several more outputs (`0,1`, `1,0`, `1,0`), the area looks like this:

```.....
..<#.
...#.
.##..
.....
```

Before you deploy the robot, you should probably have an estimate of the area it will cover: specifically, you need to know the **number of panels it paints at least once**, regardless of color. In the example above, the robot painted **6 panels** at least once. (It painted its starting panel twice, but that panel is [still only counted once](https://www.youtube.com/watch?v=KjsSvjA5TuE); it also never painted the panel it ended on.)

Build a new emergency hull painting robot and run the Intcode program on it. **How many panels does it paint at least once?**



### --- Part Two ---

You're not sure what it's trying to paint, but it's definitely not a **registration identifier**. The Space Police are getting impatient.

Checking your external ship cameras again, you notice a white panel marked "emergency hull painting robot starting panel". The rest of the panels are **still black**, but it looks like the robot was expecting to **start on a white panel**, not a black one.

Based on the Space Law Space Brochure that the Space Police attached to one of your windows, a valid registration identifier is always **eight capital letters**. After starting the robot on a single **white panel** instead, **what registration identifier does it paint** on your hull?

### [--- Solution ---](day-11.py)

```Python
# advent of code 2019
# day 11

file = 'input.txt'

class Intcode:
    def __init__(self, code): 
        self.script = tuple(code)
        self.program = {i: self.script[i] for i in range(len(self.script))}
        self.directive = 'continue'
        self.pointer = 0
        self.relative_base = 0
        self.output_value = []
        self.input_value = []
        self.verbose = False
    
    def resetComputer(self):
        self.program = {i: self.script[i] for i in range(len(self.script))}
        self.directive = 'continue'
        self.pointer = 0
        self.relative_base = 0
        self.output_value = []
        self.input_value = []
        self.verbose = False

    def printProgram(self):
        return [str(key) + ': ' + str(self.program[key]) for key in sorted(list(self.program.keys()))]

    def runProgram(self, input=[]):
        self.directive = 'continue'
        self.input_value = input
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
        if len(self.input_value) == 0:
            if self.verbose:
                print('\tinput:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), '...', sep=', ')
                print('\tno input')
            self.directive = 'pause'
        else:
            if self.verbose:
                print('\tinput:')
                print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), '...', sep=', ')
                print('\t', str(parameters[0]), ' = ', str(self.input_value[0]), sep='')
                print('\t[', str(self.identifyValue(parameters[0])), '] = ', str(self.input_value[0]), sep='')
            self.program[self.identifyValue(parameters[0])] = self.input_value[0]
            if self.verbose:
                print('\t[', str(self.identifyValue(parameters[0])), '] = ', str(self.program[self.identifyValue(parameters[0])]), sep='')
            self.input_value.pop(0)
            self.directive = 'continue'
            self.pointer += 2

    def output(self, parameters):
        if self.verbose:
            print('\toutput:')
            print('\t...', str(self.program[self.pointer]), str(self.program[self.pointer + 1]), '...', sep=', ')
            print('\t', str(self.program[self.identifyValue(parameters[0])]), sep='')
        self.output_value.append(self.program[self.identifyValue(parameters[0])])
        if self.verbose:
            print('\toutputs:', self.output_value)
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

class Hull:
    def __init__(self, computer):
        self.computer = computer
        self.direction = 'N'
        self.location = (0, 0)

    def resetHull(self):
        self.computer.resetComputer()
        self.direction = 'N'
        self.location = (0, 0)
        self.hullMap = {}

    def printMap(self):
        maxX = max([key[0] for key in self.hullMap])
        minX = min([key[0] for key in self.hullMap])
        maxY = max([key[1] for key in self.hullMap])
        minY = min([key[1] for key in self.hullMap])
        grid = [['.' for x in range(minX, maxX + 1)] for y in range(minY, maxY + 1)]
        for key in self.hullMap:
            grid[key[1] - minY][key[0] - minX] = '.' if self.hullMap[key] == 0 else '#'
        return '\n'.join(' '.join(row) for row in grid)
    
    def adjustPosition(self, instruction):
        if self.direction == 'N':
            if instruction == 0:
                self.direction = 'W'
                self.location = (self.location[0] - 1, self.location[1])
            else:
                self.direction = 'E'
                self.location = (self.location[0] + 1, self.location[1])
        elif self.direction == 'E':
            if instruction == 0:
                self.direction = 'N'
                self.location = (self.location[0], self.location[1] - 1)
            else:
                self.direction = 'S'
                self.location = (self.location[0], self.location[1] + 1)
        elif self.direction == 'S':
            if instruction == 0:
                self.direction = 'E'
                self.location = (self.location[0] + 1, self.location[1])
            else:
                self.direction = 'W'
                self.location = (self.location[0] - 1, self.location[1])
        else:
            if instruction == 0:
                self.direction = 'S'
                self.location = (self.location[0], self.location[1] + 1)
            else:
                self.direction = 'N'
                self.location = (self.location[0], self.location[1] - 1)

    def paintTile(self):
        if self.location not in self.hullMap:
            self.hullMap[self.location] = 0
        currentColor = self.hullMap[self.location]
        self.computer.runProgram([currentColor])
        newColor, movement = self.computer.output_value[-2:]
        self.hullMap[self.location] = newColor
        self.adjustPosition(movement)

    def runPaintProgram(self, initialState):
        self.hullMap = {(0, 0): initialState}
        while self.computer.directive != 'complete':
            self.paintTile()

def part_1(hull):
    hull.runPaintProgram(0)
    print('Part 1:', len(hull.hullMap))

def part_2(hull):
    hull.resetHull()
    hull.runPaintProgram(1)
    print('Part 2:', hull.printMap(), sep='\n')

def main():
    code = [int(x) for x in open(file, 'r').read().split(',')]
    emergencyHullPaintingRobot = Intcode(code)
    hull = Hull(emergencyHullPaintingRobot)
    part_1(hull)
    part_2(hull)

if __name__ == '__main__':
    main()
```