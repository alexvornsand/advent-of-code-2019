# advent of code 2019
# day 24

file = 'input.txt'

class BugMap:
    def __init__(self, map):
        self.map = {0: {}}
        self.map_states = []
        self.original_map = map

    def fillMap(self, flat=True):
        for r in range(len(self.original_map)):
            for c in range(len(self.original_map[r])):
                self.map[0][(c, r)] = self.original_map[r][c]
        if not flat:
            self.map[0].pop((2, 2))

    def printMap(self):
            for layer in sorted(list(self.map.keys())):
                print('\tlayer:', layer)
                image = ''
                for y in range(5):
                    image += '\t\t'
                    for x in range(5):
                        if (x, y) in self.map[layer]:
                            image += self.map[layer][(x, y)]
                        else:
                            image += '?'
                    image += '\n'
                print(image[:-1])

    def neighbors(self, l, x, y, flat=True):
        neighbors = []
        for true_neighbor in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if true_neighbor in self.map[l]:
                neighbors.append(self.map[l][true_neighbor])
        if not flat:
            if y == 0:
                if l - 1 in self.map:
                    neighbors.append(self.map[l - 1][(2, 1)])
            elif y == 1 and x == 2:
                if l + 1 in self.map:
                    neighbors += [self.map[l + 1][(c, 0)] for c in range(5)]
            elif y == 3 and x == 2:
                if l + 1 in self.map:
                    neighbors += [self.map[l + 1][(c, 4)] for c in range(5)]
            elif y == 4:
                if l - 1 in self.map:
                    neighbors.append(self.map[l - 1][(2, 3)])
            if x == 0:
                if l - 1 in self.map:
                    neighbors.append(self.map[l - 1][(1, 2)])
            elif x == 1 and y == 2:
                if l + 1 in self.map:
                    neighbors += [self.map[l + 1][(0, r)] for r in range(5)]
            elif x == 3 and y == 2:
                if l + 1 in self.map:
                    neighbors += [self.map[l + 1][(4, r)] for r in range(5)]
            elif x == 4:
                if l - 1 in self.map:
                    neighbors.append(self.map[l - 1][(3, 2)])
        return neighbors

    def addDropLayers(self):
        purge_list = []
        add_list = []
        for l in self.map:
            if all([value == '.' for value in self.map[l].values()]):
                purge_list.append(l)
        for l in purge_list:
            self.map.pop(l)
        for l in self.map:
            for coord in self.map[l]:
                x, y = coord
                if y in [0, 4]:
                    if l - 1 not in self.map:
                        add_list.append(l - 1)
                elif y in [1, 3] and x == 2:
                    if l + 1 not in self.map:
                        add_list.append(l + 1)
                if x in [0, 4]:
                    if l - 1 not in self.map:
                        add_list.append(l - 1)
                elif x in [1, 3] and y == 2:
                    if l + 1 not in self.map:
                        add_list.append(l + 1)
        for l in list(set(add_list)):
            self.map[l] = {coord: '.' for coord in self.map[list(self.map.keys())[0]]}

    def describeState(self):
        state = ''
        for l in sorted(list(self.map.keys())):
            state += str(l) + ':'
            for y in range(5):
                for x in range(5):
                    if (x, y) in self.map[l]:
                        state += self.map[l][(x, y)]
        return state

    def valueBiodiversity(self):
        biodiversity = sum([2 ** (5 * key[1] + key[0]) for key in self.map[0] if self.map[0][key] == '#'])
        return biodiversity

    def countBugs(self):
        return sum([self.map[l][k] == '#' for l in self.map for k in self.map[l]])

    def iterate(self, flat=True, verbose=False):
        self.map_states.append(self.describeState())
        next_map = {}
        for l in self.map:
            next_map[l] = {}
            if verbose:
                print('\tlayer:', l)
            for coord in self.map[l]:
                if verbose:
                    print('\t\tcoord:', coord)
                    print('\t\tstate:', self.map[l][coord])
                x, y = coord
                neighbors = self.neighbors(l, x, y, flat)
                if verbose:
                    print('\t\t\tneighbors:', neighbors)
                infested_neighbors = sum([neighbor == '#' for neighbor in neighbors])
                if self.map[l][coord] == '#' and infested_neighbors != 1:
                    next_map[l][coord] = '.'
                elif self.map[l][coord] == '.' and infested_neighbors in [1, 2]:
                    next_map[l][coord] = '#'
                else:
                    next_map[l][coord] = self.map[l][coord]
                if verbose:
                    print('\t\tresult:', next_map[l][coord])
                    print('\n')
        self.map = {l: {k: v for k, v in next_map[l].items()} for l in self.map}
    
def part_1(bugMap):
    bugMap.fillMap()
    while True:
        bugMap.iterate()
        if bugMap.describeState() in bugMap.map_states:
            print('Part 1:', bugMap.valueBiodiversity())
            break


def part_2(bugMap):
    bugMap.fillMap(False)
    for i in range(200):
        bugMap.addDropLayers()
        bugMap.iterate(flat=False)
    print('Part 2:', bugMap.countBugs())

def main():
    map = [[c for c in r] for r in open(file, 'r').read().splitlines()]
    bugMap = BugMap(map)
    part_1(bugMap)
    part_2(bugMap)

if __name__ == '__main__':
    main()
