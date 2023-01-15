### [--- Day 15: Oxygen System ---](https://adventofcode.com/2019/day/15)

Out here in deep space, many things can go wrong. Fortunately, many of those things have indicator lights. Unfortunately, one of those lights is lit: the oxygen system for part of the ship has failed!

According to the readouts, the oxygen system must have failed days ago after a rupture in oxygen tank two; that section of the ship was automatically sealed once oxygen levels went dangerously low. A single remotely-operated **repair droid** is your only option for fixing the oxygen system.

The Elves' care package included an [Intcode](../day-09) program (your puzzle input) that you can use to remotely control the repair droid. By running that program, you can direct the repair droid to the oxygen system and fix the problem.

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

# part 1
intCode = [int(x) for x in open('input.txt', 'r').read()[:-1].split(',')]

def navigateMaze(intCode, partTwo=False):
    def evaluatePath(intCode, c, base, path):
        code = intCode.copy()
        output = 1
        while(True):
            paddedC = str(code[c]).zfill(5)
            opcode = int(paddedC[-2:])
            pm1, pm2, pm3 = [int(d) for d in paddedC[:3]][::-1]
            if opcode in [1, 2, 7, 8]: # three-parameter codes
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0
                if pm2 == 0:
                    p2Loc = code[c + 2]
                elif pm2 == 1:
                    p2Loc = c + 2
                else:
                    p2Loc = base + code[c + 2]
                if p2Loc not in code.keys(): code[p2Loc] = 0
                if pm3 == 0:
                    p3Loc = code[c + 3]
                elif pm3 == 1:
                    p3Loc = c + 3
                else:
                    p3Loc = base + code[c + 3]
                if p3Loc not in code.keys(): code[p3Loc] = 0

                # execute code
                if opcode == 1: # addition 
                    code[p3Loc] = code[p1Loc] + code[p2Loc]
                elif opcode == 2: # multiplication 
                    code[p3Loc] = code[p1Loc] * code[p2Loc]
                elif opcode == 7: # less-than 
                    code[p3Loc] = 1 if code[p1Loc] < code[p2Loc] else 0        
                else: # equality 
                    code[p3Loc] = 1 if code[p1Loc] == code[p2Loc] else 0
                c += 4

            elif opcode in [5, 6]: # jump codes
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0
                if pm2 == 0:
                    p2Loc = code[c + 2]
                elif pm2 == 1:
                    p2Loc = c + 2
                else:
                    p2Loc = base + code[c + 2]
                if p2Loc not in code.keys(): code[p2Loc] = 0

                # execute code
                if opcode == 5: # jump if true
                    c = code[p2Loc] if code[p1Loc] != 0 else c + 3
                else: # jump if false
                    c = code[p2Loc] if code[p1Loc] == 0 else c + 3

            elif opcode == 3: # read
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0

                # execute code
                if len(path) > 0:
                    code[p1Loc] = path[0]
                    path.pop(0)
                    c += 2
                else:
                    return(output, code, c, base)

            elif opcode == 4: # write
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0

                # execute code
                output = code[p1Loc]
                c += 2
            elif opcode == 9: # shift base
                # assign parameter values
                if pm1 == 0: 
                    p1Loc = code[c + 1]
                elif pm1 == 1:
                    p1Loc = c + 1
                else:
                    p1Loc = base + code[c + 1]
                if p1Loc not in code.keys(): code[p1Loc] = 0

                # execute code
                base += code[p1Loc]
                c += 2
            else:
                break
        return(output)
    def printMap(mapNodes):
        minY = min([key[0] for key in mapNodes])
        maxY = max([key[0] for key in mapNodes])
        minX = min([key[1] for key in mapNodes])
        maxX = max([key[1] for key in mapNodes])
        image = ''
        for y in range(minY, maxY + 1):
            for x in range(minX, maxX + 1):
                if (y, x) in mapNodes:
                    image += mapNodes[(y, x)]['state']
                else:
                    image += ' '
            image += '\n'
        print(image)
    code = {i: intCode[i] for i in range(len(intCode))}    
    mapNodes = {(0, 0): {
        'path': [], 
        'len': 0, 
        'state': 'S', 
        'visited': False, 
        'intCode': code.copy(), 
        'c': 0, 
        'base': 0, 
        'oxygen': False,
        'timeToO2': 999999}}
    queue = [(0, 0)]
    responseKey = {0: '#', 1: '.', 2: 'o'}
    while(True):
        nextQueue = set()
        for node in queue:
            r, c = node
            for neighbor in [(r - 1, c, 1), (r + 1, c, 2), (r, c - 1, 3), (r, c + 1, 4)]:
                y, x, d = neighbor
                if (y, x) in mapNodes:
                    mapNodes[(y, x)]['len'] = min(mapNodes[node]['len'] + 1, mapNodes[(y, x)]['len'])
                else:
                    neighborIntCode = mapNodes[node]['intCode'].copy()
                    neighborC = mapNodes[node]['c']
                    neighborBase = mapNodes[node]['base']
                    neighborPath = mapNodes[node]['path'].copy() + [d]
                    resultOutput, resultIntCode, resultC, resultBase = evaluatePath(neighborIntCode, neighborC, neighborBase, [d])
                    mapNodes[(y, x)] = {
                        'path': neighborPath,
                        'len': len(neighborPath),
                        'state': responseKey[resultOutput],
                        'visited': False,
                        'intCode': resultIntCode,
                        'c': resultC,
                        'base': resultBase,
                        'oxygen': responseKey[resultOutput] == 'o',
                        'timeToO2': 0
                    }
                    if resultOutput != 0:
                        nextQueue.add((y, x))
            mapNodes[node]['visited'] = True
        if len(nextQueue) > 0:
            queue = nextQueue
        else:
            oxygenSource = [key for key in mapNodes if mapNodes[key]['state'] == 'o'][0]
            if partTwo is False:
                return(mapNodes[oxygenSource]['len'])
            else:
                currentNode = oxygenSource
                queue = [oxygenSource]
                while(True):
                    nextQueue = set()
                    for node in queue:
                        r, c = node
                        for neighbor in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                            y, x = neighbor
                            if (y, x) in mapNodes and mapNodes[(y, x)]['state'] != '#' and mapNodes[(y, x)]['oxygen'] is False:
                                mapNodes[(y, x)]['oxygen'] = True
                                mapNodes[(y, x)]['timeToO2'] = mapNodes[node]['timeToO2'] + 1
                                nextQueue.add((y, x))
                    if len(nextQueue) == 0:
                        return(mapNodes[node]['timeToO2'])
                    else:
                        queue = nextQueue

navigateMaze(intCode)

# part 2
navigateMaze(intCode)
```