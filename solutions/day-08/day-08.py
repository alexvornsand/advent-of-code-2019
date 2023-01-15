# advent of code 2019
# day 8

# part 1
import numpy as np

transmission = open('input.txt', 'r').read()[:-1]

def parseImage(transmission, partTwo=False):
    layers = [transmission[i * (25 * 6):i * (25 * 6) + (25 * 6)] for i in range(int(len(transmission) / (25 * 6)))]  
    sortedLayers = sorted(layers, key=lambda l: len([d for d in l if d == '0']))
    if partTwo is False:
        return(len([d for d in sortedLayers[0] if d == '1']) * len([d for d in sortedLayers[0] if d == '2']))
    else:
        layerGrid = [np.array([int(c) for c in l]).reshape(6, 25) for l in layers]
        i = np.array([[2] * 25] * 6)
        layers = [np.array(l) for l in layers]
        for y in range(6):
            for x in range(25):
                p = 2
                for l in range(int(len(transmission) / (25 * 6))):
                    if layerGrid[l][y][x] == 2:
                        pass
                    else:
                        p = int(layerGrid[l][y][x])
                        break                    
                i[y][x] = p
        print('\n'.join([''.join([' ' if d == 0 else '#' for d in l]) for l in i]))

parseImage(transmission)

# part 2
parseImage(transmission, True)
