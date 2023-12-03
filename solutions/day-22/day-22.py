# advent of code 2019
# day 22

file = 'input.txt'

class Deck:
    def __init__(self, N=10007):
        self.N = N
    
    def composeFunctions(self, f, g):
        a, b = f
        c, d = g
        return (a*c % self.N, (a*d + b) % self.N)

    def buildShuffleFuncton(self, instructions):
        composite_function = (1, 0)
        for instruction in instructions:
            if 'stack' in instruction:
                composite_function = self.composeFunctions((-1, -1), composite_function)
            elif 'cut' in instruction:
                param = int(instruction.split(' ')[-1])
                composite_function = self.composeFunctions((1, -param), composite_function)
            else:
                param = int(instruction.split(' ')[-1])
                composite_function = self.composeFunctions((param, 0), composite_function)
        return composite_function
    
    def evaluateFunction(self, index, function):
        a, b = function
        return (a * index + b) % self.N
    
    def recomposeFunction(self, function, k):
        f = list(function)
        g = [1, 0]
        while k > 0:
            if k % 2 == 1:
                g = self.composeFunctions(g, f)
            k = k // 2
            f = self.composeFunctions(f, f)
        return g
    
    def inverseFunction(self, function, x):
        A, B = function
        return ((x - B) % self.N) * (pow(A, -1, self.N) % self.N) % self.N
    
def part_1(instructions):
    deck = Deck()
    print('Part 1:', deck.evaluateFunction(2019, deck.buildShuffleFuncton(instructions)))

def part_2(instructions):
    deck = Deck(N=119315717514047)
    print('Part 2:', deck.inverseFunction(deck.recomposeFunction(deck.buildShuffleFuncton(instructions), 101741582076661), 2020))

def main():
    instructions = open(file, 'r').read().splitlines()
    part_1(instructions)
    part_2(instructions)

if __name__ == '__main__':
    main()