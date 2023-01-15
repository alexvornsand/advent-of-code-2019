# advent of code 2019
# day 10

# part 1
import math

map = [[x for x in r] for r in open('input.txt', 'r').read()[:-1].split('\n')]

def chooseOptimalAsteroid(map, partTwo=False):
    allAsteroids = {}
    astId = 0
    for r in range(len(map)):
        for c in range(len(map[0])):
            if map[r][c] == '.':
                allAsteroids[(c, r)] = '.'
            else:
                allAsteroids[(c, r)] = '#'
    def plotMap(allAsteroids, candidate):
        asteroids = {}
        for asteroid in allAsteroids.keys():
            asteroids[(asteroid[0] - candidate[0], asteroid[1] - candidate[1])] = allAsteroids[asteroid]
        angleDict = {}
        for asteroid in asteroids.keys():
            if asteroids[asteroid] == '#' and asteroid != (0,0):
                angle = math.atan2(asteroid[1], asteroid[0]) + math.pi / 2
                angle = angle + 2 * math.pi if angle < 0 else angle
                coords = [asteroid[0] + candidate[0], asteroid[1] + candidate[1]]
                if angle not in angleDict.keys():
                    angleDict[angle] = [coords]
                else:
                    angleDict[angle] += [coords]
        angleDict = dict(sorted(angleDict.items()))
        for angle in angleDict:
            angleDict[angle] = sorted(angleDict[angle], key=lambda c: math.sqrt((c[0] - candidate[0]) ** 2 + (c[1] - candidate[1]) ** 2))
        laps = max([len(coordList) for coordList in angleDict.values()])
        lapsDict = {}
        for i in range(laps):
            lapsDict[i] = []
        for angle in sorted(angleDict.keys()):
            for i in range(len(angleDict[angle])):
                lapsDict[i] += [angleDict[angle][i]]
        laserSequence = []
        for i in range(laps):
            laserSequence += lapsDict[i]
        twoHundreth = laserSequence[199]
        coordProd = twoHundreth[0] * 100 + twoHundreth[1]
        return(coordProd * 10000 + len(angleDict.values()))
    visibilityResults = [plotMap(allAsteroids, ast) for ast in allAsteroids if allAsteroids[ast] == '#']
    highestVisibility = sorted(visibilityResults, key=lambda n: n - (10000 * math.floor(n / 10000)), reverse=True)[0]
    if partTwo is False:
        return(highestVisibility - 10000 * math.floor(highestVisibility / 10000))
    else:
        return(math.floor(highestVisibility / 10000))

chooseOptimalAsteroid(map)

# part 2
chooseOptimalAsteroid(map, True)