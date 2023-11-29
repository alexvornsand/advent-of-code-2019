### [--- Day 15: Oxygen System ---](https://adventofcode.com/2019/day/15)

Out here in deep space, many things can go wrong. Fortunately, many of those things have indicator lights. Unfortunately, one of those lights is lit: the oxygen system for part of the ship has failed!

According to the readouts, the oxygen system must have failed days ago after a rupture in oxygen tank two; that section of the ship was automatically sealed once oxygen levels went dangerously low. A single remotely-operated **repair droid** is your only option for fixing the oxygen system.

The Elves' care package included an [Intcode](https://adventofcode.com/2019/day/9) program (your puzzle input) that you can use to remotely control the repair droid. By running that program, you can direct the repair droid to the oxygen system and fix the problem.

The remote control program executes the following steps in a loop forever:

- Accept a **movement command** via an input instruction.
- Send the movement command to the repair droid.
- Wait for the repair droid to finish the movement operation.
- Report on the **status** of the repair droid via an output instruction.

Only four **movement commands** are understood: north (`1`), south (`2`), west (`3`), and east (`4`). Any other command is invalid. The movements differ in direction, but not in distance: in a long enough east-west hallway, a series of commands like `4,4,4,4,3,3,3,3` would leave the repair droid back where it started.

The repair droid can reply with any of the following **status** codes:

- `0`: The repair droid hit a wall. Its position has not changed.
- `1`: The repair droid has moved one step in the requested direction.
- `2`: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.

You don't know anything about the area around the repair droid, but you can figure it out by watching the status codes.

For example, we can draw the area using `D` for the droid, `#` for walls, `.` for locations the droid can traverse, and empty space for unexplored locations. Then, the initial state looks like this:

```
      
      
   D  
      
      
```
To make the droid go north, send it `1`. If it replies with `0`, you know that location is a wall and that the droid didn't move:

```
      
   #  
   D  
      
      
```
To move east, send `4`; a reply of `1` means the movement was successful:

```
      
   #  
   .D 
      
```      
Then, perhaps attempts to move north (`1`), south (`2`), and east (`4`) are all met with replies of `0`:

```
      
   ## 
   .D#
    # 
      
```
Now, you know the repair droid is in a dead end. Backtrack with `3` (which you already know will get a reply of `1` because you already know that location is open):

```
      
   ## 
   D.#
    # 
      
```
Then, perhaps west (`3`) gets a reply of `0`, south (`2`) gets a reply of `1`, south again (`2`) gets a reply of `0`, and then west (`3`) gets a reply of `2`:

```
      
   ## 
  #..#
  D.# 
   #  
```
Now, because of the reply of `2`, you know you've found the **oxygen system**! In this example, it was only 2 moves away from the repair droid's starting position.

**What is the fewest number of movement commands** required to move the repair droid from its starting position to the location of the oxygen system?

### --- Part Two ---

You quickly repair the oxygen system; oxygen gradually fills the area.

Oxygen starts in the location containing the repaired oxygen system. It takes **one minute** for oxygen to spread to all open locations that are adjacent to a location that already contains oxygen. Diagonal locations are **not** adjacent.

In the example above, suppose you've used the droid to explore the area fully and have the following map (where locations that currently contain oxygen are marked `O`):

```
 ##   
#..## 
#.#..#
#.O.# 
 ###  
```
Initially, the only location which contains oxygen is the location of the repaired oxygen system. However, after one minute, the oxygen spreads to all open (`.`) locations that are adjacent to a location containing oxygen:

```
 ##   
#..## 
#.#..#
#OOO# 
 ###  
```
After a total of two minutes, the map looks like this:

```
 ##   
#..## 
#O#O.#
#OOO# 
 ###  
```
After a total of three minutes:

```
 ##   
#O.## 
#O#OO#
#OOO# 
 ###  
```
And finally, the whole region is full of oxygen after a total of four minutes:

```
 ##   
#OO## 
#O#OO#
#OOO# 
 ###  
```
So, in this example, all locations contain oxygen after `4` minutes.

Use the repair droid to get a complete map of the area. **How many minutes will it take to fill with oxygen?**

### [--- Solution ---](day-15.py)
```Python
# advent of code 2019
# day 15

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

class OxygenRoom:
    def __init__(self):
        self.map = {(0, 0): 1}
        self.time_map = {}

    def exploreRoom(self, explorer: Intcode):
        explorer.resetComputer()
        program_state = {}
        pointer = {}
        base = {}
        unvisited = []
        visited = []
        location = (0, 0)
        explorer.runProgram()
        program_state[location] = {k: v for k, v in explorer.program.items()}
        pointer[location] = explorer.pointer
        base[location] = explorer.relative_base
        unvisited += [(0, 1), (1, 0), (0, -1), (-1, 0)]
        visited.append([(0, 0)])
        while len(unvisited) > 0:
            next_neighbor = unvisited[0]
            next_x, next_y = next_neighbor
            if (next_x, next_y + 1) in program_state:
                travel_from = (next_x, next_y + 1)
                input = 1
            elif (next_x, next_y - 1) in program_state:
                travel_from = (next_x, next_y - 1)
                input = 2
            elif (next_x + 1, next_y) in program_state:
                travel_from = (next_x + 1, next_y)
                input = 3
            elif (next_x - 1, next_y) in program_state:
                travel_from = (next_x - 1, next_y)
                input = 4
            else:
                break
            explorer.clearOutput()
            explorer.program = {k: v for k, v in program_state[travel_from].items()}
            explorer.pointer = pointer[travel_from]
            explorer.relative_base = base[travel_from]
            explorer.runProgram([input])
            result = explorer.output_values[-1]
            self.map[next_neighbor] = result
            if result != 0:
                for location in [(next_x + 1, next_y), (next_x - 1, next_y), (next_x, next_y + 1), (next_x, next_y - 1)]:
                    if location not in visited and location not in unvisited:
                        unvisited.append(location)        
                visited.append(next_neighbor)
                location = next_neighbor
                program_state[location] = {k: v for k, v in explorer.program.items()}
                pointer[location] = explorer.pointer
                base[location] = explorer.relative_base
            unvisited.remove(next_neighbor)
        
    def fillRoomWithOxygen(self):
        timer = 0
        unvisited_nodes = [coord for coord in self.map if self.map[coord] > 0]
        visited_nodes = []
        queue = [list(self.map.keys())[list(self.map.values()).index(2)]]
        while len(unvisited_nodes) > 0:
            next_queue = []
            for coord in queue:
                x, y = coord
                self.time_map[coord] = timer
                visited_nodes.append(coord)
                unvisited_nodes.remove(coord)
                for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if neighbor in unvisited_nodes and neighbor not in queue:
                        next_queue.append(neighbor)
            timer += 1
            queue = next_queue

def part_1(oxygenRoom):
    print('Part 1:', oxygenRoom.time_map[(0, 0)])

def part_2(oxygenRoom):
    print('Part 2:', max(oxygenRoom.time_map.values()))

def main():
    code = [int(x) for x in open(file, 'r').read().split(',')]
    explorer = Intcode(code)
    oxygenRoom = OxygenRoom()
    oxygenRoom.exploreRoom(explorer)
    oxygenRoom.fillRoomWithOxygen()
    part_1(oxygenRoom)
    part_2(oxygenRoom)

if __name__ == '__main__':
    main()
```