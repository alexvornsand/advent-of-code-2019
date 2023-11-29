### [--- Day 17: Set and Forget ---](https://adventofcode.com/2019/day/17)

An early warning system detects an incoming [solar flare](https://en.wikipedia.org/wiki/Solar_flare) and automatically activates the ship's electromagnetic shield. Unfortunately, this has cut off the Wi-Fi for many small robots that, unaware of the impending danger, are now trapped on exterior scaffolding on the unsafe side of the shield. To rescue them, you'll have to act quickly!

The only tools at your disposal are some wired cameras and a small vacuum robot currently asleep at its charging station. The video quality is poor, but the vacuum robot has a needlessly bright LED that makes it easy to spot no matter where it is.

An [Intcode](https://adventofcode.com/2019/day/9) program, the **Aft Scaffolding Control and Information Interface** (ASCII, your puzzle input), provides access to the cameras and the vacuum robot. Currently, because the vacuum robot is asleep, you can only access the cameras.

Running the ASCII program on your Intcode computer will provide the current view of the scaffolds. This is output, purely coincidentally, as [ASCII code](https://simple.wikipedia.org/wiki/ASCII): `35` means `#`, `46` means `.`, `10` starts a [new line](https://en.wikipedia.org/wiki/Newline#In_programming_languages) of output below the current one, and so on. (Within a line, characters are drawn left-to-right.)

In the camera output, `#` represents a scaffold and `.` represents open space. The vacuum robot is visible as `^`, `v`, `<`, or `>` depending on whether it is facing up, down, left, or right respectively. When drawn like this, the vacuum robot is **always on a scaffold**; if the vacuum robot ever walks off of a scaffold and begins **tumbling through space uncontrollably**, it will instead be visible as `X`.

In general, the scaffold forms a path, but it sometimes loops back onto itself. For example, suppose you can see the following view from the cameras:

```
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..
```
Here, the vacuum robot, `^` is facing up and sitting at one end of the scaffold near the bottom-right of the image. The scaffold continues up, loops across itself several times, and ends at the top-left of the image.

The first step is to calibrate the cameras by getting the **alignment parameters** of some well-defined points. Locate all **scaffold intersections**; for each, its alignment parameter is the distance between its left edge and the left edge of the view multiplied by the distance between its top edge and the top edge of the view. Here, the intersections from the above image are marked `O`:

```
..#..........
..#..........
##O####...###
#.#...#...#.#
##O###O###O##
..#...#...#..
..#####...^..
```
For these intersections:

- The top-left intersection is `2` units from the left of the image and `2` units from the top of the image, so its alignment parameter is `2 * 2 = 4`.
- The bottom-left intersection is `2` units from the left and `4` units from the top, so its alignment parameter is `2 * 4 = 8`.
- The bottom-middle intersection is `6` from the left and `4` from the top, so its alignment parameter is `24`.
- The bottom-right intersection's alignment parameter is `40`.

To calibrate the cameras, you need the **sum of the alignment parameters**. In the above example, this is **`76`**.

Run your ASCII program. **What is the sum of the alignment parameters** for the scaffold intersections?

### --- Part Two ---

Now for the tricky part: notifying all the other robots about the solar flare. The vacuum robot can do this automatically if it gets into range of a robot. However, you can't see the other robots on the camera, so you need to be thorough instead: you need to make the vacuum robot **visit every part of the scaffold at least once**.

The vacuum robot normally wanders randomly, but there isn't time for that today. Instead, you can **override its movement logic** with new rules.

Force the vacuum robot to wake up by changing the value in your ASCII program at address `0` from `1` to **`2`**. When you do this, you will be automatically prompted for the new movement rules that the vacuum robot should use. The ASCII program will use input instructions to receive them, but they need to be provided as ASCII code; end each line of logic with a single newline, ASCII code `10`.

First, you will be prompted for the **main movement routine**. The main routine may only call the **movement functions**: `A`, `B`, or `C`. Supply the movement functions to use as ASCII text, separating them with commas (`,`, ASCII code `44`), and ending the list with a newline (ASCII code `10`). For example, to call `A` twice, then alternate between `B` and `C` three times, provide the string `A,A,B,C,B,C,B,C` and then a newline.

Then, you will be prompted for each **movement function**. Movement functions may use `L` to **turn left**, `R` to **turn right**, or a number to **move forward** that many units. Movement functions may not call other movement functions. Again, separate the actions with commas and end the list with a newline. For example, to move forward `10` units, turn left, move forward `8` units, turn right, and finally move forward `6` units, provide the string `10,L,8,R,6` and then a newline.

Finally, you will be asked whether you want to see a **continuous video feed**; provide either `y` or `n` and a newline. Enabling the continuous video feed can help you see what's going on, but it also requires a significant amount of processing power, and may even cause your Intcode computer to overheat.

Due to the limited amount of memory in the vacuum robot, the ASCII definitions of the main routine and the movement functions may each contain **at most 20 characters**, not counting the newline.

For example, consider the following camera feed:

```
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......
```
In order for the vacuum robot to **visit every part of the scaffold at least once**, one path it could take is:

```
R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2
```
Without the memory limit, you could just supply this whole string to function `A` and have the main routine call `A` once. However, you'll need to split it into smaller parts.

One approach is:

- **Main routine**: **`A,B,C,B,A,C`**
    (ASCII input: `65`, `44`, `66`, `44`, `67`, `44`, `66`, `44`, `65`, `44`, `67`, `10`)
- **Function A**:   **`R,8,R,8`**
    (ASCII input: `82`, `44`, `56`, `44`, `82`, `44`, `56`, `10`)
- **Function B**:   **`R,4,R,4,R,8`**
    (ASCII input: `82`, `44`, `52`, `44`, `82`, `44`, `52`, `44`, `82`, `44`, `56`, `10`)
- **Function C**:   **`L,6,L,2`**
    (ASCII input: `76`, `44`, `54`, `44`, `76`, `44`, `50`, `10`)

Visually, this would break the desired path into the following parts:

```
A,        B,            C,        B,            A,        C
R,8,R,8,  R,4,R,4,R,8,  L,6,L,2,  R,4,R,4,R,8,  R,8,R,8,  L,6,L,2

CCCCCCA...BBBBB
C.....A...B...B
C.....A...B...B
......A...B...B
......A...CCC.B
......A.....C.B
^AAAAAAAA...C.B
......A.A...C.B
......AAAAAA#AB
........A...C..
....BBBB#BBBB..
....B...A......
....B...A......
....B...A......
....BBBBA......
```
Of course, the scaffolding outside your ship is much more complex.

As the vacuum robot finds other robots and notifies them of the impending solar flare, it also can't help but leave them squeaky clean, collecting any space dust it finds. Once it finishes the programmed set of movements, assuming it hasn't drifted off into space, the cleaning robot will return to its docking station and report the amount of space dust it collected as a large, non-ASCII value in a single output instruction.

After visiting every part of the scaffold at least once, **how much dust does the vacuum robot report it has collected?**

### [--- Solution ---](day-17.py)

```Python
# advent of code 2019
# day 17

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

def part_1(ASCII):
    grid = [[x for x in line] for line in ''.join([chr(x) for x in ASCII.output_values]).split()]
    map = {}
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            map[(c, r)] = grid[r][c]
    intersections = 0
    for coord in map:
        if map[coord] == '#':
            x, y = coord
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            if all([neighbor in map and map[neighbor] == '#' for neighbor in neighbors]):
                intersections += x * y
    print('Part 1:', intersections)

def part_2(ASCII):
    ASCII.resetComputer()
    ASCII.program[0] = 2
    main = 'A,B,A,C,A,B,C,C,A,B'
    A = 'R,8,L,10,R,8'
    B = 'R,12,R,8,L,8,L,12'
    C = 'L,12,L,10,L,8'
    input = [ord(d) for d in main] + [ord('\n')]
    input += eval('[' + (',' + str(ord(',')) + ',').join([','.join([str(ord(x)) for x in a]) for a in A.split(',')]) + ']') + [ord('\n')]
    input += eval('[' + (',' + str(ord(',')) + ',').join([','.join([str(ord(x)) for x in b]) for b in B.split(',')]) + ']') + [ord('\n')]
    input += eval('[' + (',' + str(ord(',')) + ',').join([','.join([str(ord(x)) for x in c]) for c in C.split(',')]) + ']') + [ord('\n')]
    input += [ord('n'), ord('\n')]
    ASCII.runProgram(input)
    print('Part 2:', ASCII.output_values[-1])

def main():
    code = [int(x) for x in open(file, 'r').read().split(',')]
    ASCII = Intcode(code)
    ASCII.runProgram()
    part_1(ASCII)
    part_2(ASCII)

if __name__ == '__main__':
    main()
```