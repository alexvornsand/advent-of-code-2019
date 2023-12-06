# advent of code 2019
# day 20

file = 'input.txt'

class PlutoMap():
    def __init__(self):
        self.map = {}
        self.portals = {}
        self.terminals = {}

    def fillMap(self, input):
        for r in range(len(input)):
            for c in range(len(input[r])):
                self.map[(c, r)] = input[r][c]
        portals = {}
        width = len(input[0])
        length = len(input)
        for coord in self.map:
            x, y = coord
            if self.map[coord] not in ['.', '#', ' ']:
                if (x - 1, y) in self.map and self.map[(x - 1, y)] == '.':
                    # coming from the left
                    name = self.map[coord] + self.map[(x + 1, y)]
                    if name not in ['AA', 'ZZ']:
                        if name in portals:
                            if x < width / 2:
                                portals[name][1] = (x - 1, y)
                            else:
                                portals[name][-1] = (x - 1, y)                                
                        else:
                            if x < width / 2:
                                portals[name] = {1: (x - 1, y)}
                            else:
                                portals[name] = {-1: (x - 1, y)}
                        self.map[coord] = 'P'
                        self.map[(x + 1, y)] = ' '
                    else:
                        self.terminals[name] = (x - 1, y)
                        self.map[coord] = ' '
                        self.map[(x + 1, y)] = ' '
                elif (x + 1, y) in self.map and self.map[(x + 1, y)] == '.':
                    # coming from the right
                    name =  self.map[(x - 1, y)] + self.map[coord]
                    if name not in ['AA', 'ZZ']:
                        if name in portals:
                            if x < width / 2:
                                portals[name][-1] = (x + 1, y)
                            else:
                                portals[name][1] = (x + 1, y)                                
                        else:
                            if x < width / 2:
                                portals[name] = {-1: (x + 1, y)}
                            else:
                                portals[name] = {1: (x + 1, y)}
                        self.map[coord] = 'P'
                        self.map[(x - 1, y)] = ' '
                    else:
                        self.terminals[name] = (x + 1, y)
                        self.map[coord] = ' '
                        self.map[(x - 1, y)] = ' '
                elif (x, y - 1) in self.map and self.map[(x, y - 1)] == '.':
                    # coming from above
                    name = self.map[coord] + self.map[(x, y + 1)]
                    if name not in ['AA', 'ZZ']:
                        if name in portals:
                            if y < length / 2:
                                portals[name][1] = (x, y - 1)
                            else:
                                portals[name][-1] = (x, y - 1)                                
                        else:
                            if y < length / 2:
                                portals[name] = {1: (x, y - 1)}
                            else:
                                portals[name] = {-1: (x, y - 1)}
                        self.map[coord] = 'P'
                        self.map[(x, y + 1)] = ' '
                    else:
                        self.terminals[name] = (x, y - 1)
                        self.map[coord] = ' '
                        self.map[(x, y + 1)] = ' '
                elif (x, y + 1) in self.map and self.map[(x, y + 1)] == '.':
                    # coming from below
                    name =  self.map[(x, y - 1)] + self.map[coord]
                    if name not in ['AA', 'ZZ']:
                        if name in portals:
                            if y < length / 2:
                                portals[name][-1] = (x, y + 1)
                            else:
                                portals[name][1] = (x, y + 1)                                
                        else:
                            if y < length / 2:
                                portals[name] = {-1: (x, y + 1)}
                            else:
                                portals[name] = {1: (x, y + 1)}
                        self.map[coord] = 'P'
                        self.map[(x, y - 1)] = ' '
                    else:
                        self.terminals[name] = (x, y + 1)
                        self.map[coord] = ' '
                        self.map[(x, y - 1)] = ' '
        for portal in portals:
            self.portals[portals[portal][1]] = tuple([1] + list(portals[portal][-1]))
            self.portals[portals[portal][-1]] = tuple([-1] + list(portals[portal][1]))

    def printMap(self):
        x_min = min([key[0] for key in self.map])
        x_max = max([key[0] for key in self.map])
        y_min = min([key[1] for key in self.map])
        y_max = max([key[1] for key in self.map])
        image = ''
        image += '  '
        for x in range(x_min, x_max + 1):
            if x % 5 == 0:
                image += str(x).rjust(5, ' ')
        image += '\n'
        for y in range(y_min, y_max + 1):
            if y % 5 == 0:
                image += str(y).rjust(5, ' ') + ' '
            else:
                image += '      '
            for x in range(x_min, x_max + 1):
                image += self.map[(x, y)]
            if y % 5 == 0:
                image += str(y).rjust(5, ' ') + ' '
            else:
                image += '      '
            image += '\n'
        image += '  '
        for x in range(x_min, x_max + 1):
            if x % 5 == 0:
                image += str(x).rjust(5, ' ')
        print(image)

    def portalHop(self, l, x, y, flat=True):
        neighbor_l, neighbor_x, neighbor_y = self.portals[(x, y)]
        if not flat:
            if l == 0 and neighbor_l == -1:
                return (l, x, y)
            else:
                return (l + neighbor_l, neighbor_x, neighbor_y)
        else:
            return (l, neighbor_x, neighbor_y)

    def neighbors(self, l, x, y, flat=True):
        neighbors = []
        for neighbor in [(l, x - 1, y), (l, x + 1, y), (l, x, y - 1), (l, x, y + 1)]:
            if self.map[neighbor[1:]] == '.':
                neighbors.append(neighbor)
            elif self.map[neighbor[1:]] == 'P':
                neighbors.append(self.portalHop(l, x, y, flat))
        return neighbors
                        
    def navigateMaze(self, flat=True, verbose=False):
        visited_nodes = []
        queue = []
        current_node = tuple([0] + list(self.terminals['AA']))
        terminal_node = tuple([0] + list(self.terminals['ZZ']))
        distances = {}
        distances[current_node] = 0
        while True:
            l, x, y = current_node
            if verbose:
                print('current node:', current_node)
                print(distances[current_node])
            for neighbor in self.neighbors(l, x, y, flat):
                if neighbor not in visited_nodes:
                    if verbose:
                        print('\tneighbor:', neighbor)
                    if neighbor in distances:
                        distances[neighbor] = min(distances[current_node] + 1, distances[neighbor])
                    else:
                        distances[neighbor] = distances[current_node] + 1
                    if verbose:
                        print('\t', distances[neighbor], sep='')
                    if neighbor not in queue:
                        queue.append(neighbor)
            visited_nodes.append(current_node)
            if current_node == terminal_node:
                return distances[current_node]
            else:                
                current_node = queue[0]
                queue.remove(current_node)

def part_1(plutoMap):
    plutoMap.fillMap(map)
    print('Part 1:', plutoMap.navigateMaze())

def part_2(plutoMap):
    plutoMap.fillMap(map)
    print('Part 2:', plutoMap.navigateMaze(False))

def main():
    map = [[c for c in r] for r in open(file, 'r').read().splitlines()]
    plutoMap = PlutoMap()
    part_1(plutoMap)
    part_2(plutoMap)

if __name__ == '__main__':
    main()