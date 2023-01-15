# advent of code 2019
# day 12

# part 1
import re
import math

moons = open('input.txt', 'r').read()[:-1].split('\n')

def analyzeOrbits(moons, partTwo=False):
    moonDict = {}
    for i in range(len(moons)):
        coords = re.match('<x=(.*),\sy=(.*),\sz=(.*)>', moons[i]).groups()
        moonDict[i] = {
            'pX': int(coords[0]),
            'pY': int(coords[1]),
            'pZ': int(coords[2]),
            'vX': 0,
            'vY': 0,
            'vZ': 0
        }

    # loop x through time
    t = 0
    xOrig = (moonDict[0]['pX'], moonDict[0]['vX'], moonDict[1]['pX'], moonDict[1]['vX'], moonDict[2]['pX'], moonDict[2]['vX'], moonDict[3]['pX'], moonDict[3]['vX'])
    while(True):
        if t == 1000 and partTwo is False:
            break
        for i in range(len(moonDict.keys()) - 1):
            for j in range(i + 1, len(moonDict.keys())):
                if moonDict[i]['pX'] < moonDict[j]['pX']:
                    moonDict[i]['vX'] += 1
                    moonDict[j]['vX'] -= 1
                elif moonDict[i]['pX'] > moonDict[j]['pX']:
                    moonDict[i]['vX'] -= 1
                    moonDict[j]['vX'] += 1
        for moon in moonDict.keys():
            moonDict[moon]['pX'] += moonDict[moon]['vX']
        xState = (moonDict[0]['pX'], moonDict[0]['vX'], moonDict[1]['pX'], moonDict[1]['vX'], moonDict[2]['pX'], moonDict[2]['vX'], moonDict[3]['pX'], moonDict[3]['vX'])
        if partTwo is True and xState == xOrig:
            xCycleLength = t + 1
            break
        else:
            t += 1

    # loop y through time
    t = 0
    yOrig = (moonDict[0]['pY'], moonDict[0]['vY'], moonDict[1]['pY'], moonDict[1]['vY'], moonDict[2]['pY'], moonDict[2]['vY'], moonDict[3]['pY'], moonDict[3]['vY'])
    while(True):
        if t == 1000 and partTwo is False:
            break
        for i in range(len(moonDict.keys()) - 1):
            for j in range(i + 1, len(moonDict.keys())):
                if moonDict[i]['pY'] < moonDict[j]['pY']:
                    moonDict[i]['vY'] += 1
                    moonDict[j]['vY'] -= 1
                elif moonDict[i]['pY'] > moonDict[j]['pY']:
                    moonDict[i]['vY'] -= 1
                    moonDict[j]['vY'] += 1
        for moon in moonDict.keys():
            moonDict[moon]['pY'] += moonDict[moon]['vY']
        yState = (moonDict[0]['pY'], moonDict[0]['vY'], moonDict[1]['pY'], moonDict[1]['vY'], moonDict[2]['pY'], moonDict[2]['vY'], moonDict[3]['pY'], moonDict[3]['vY'])
        if partTwo is True and yState == yOrig:
            yCycleLength = t + 1
            break
        else:
            t += 1

    # loop z through time
    t = 0
    zOrig = (moonDict[0]['pZ'], moonDict[0]['vZ'], moonDict[1]['pZ'], moonDict[1]['vZ'], moonDict[2]['pZ'], moonDict[2]['vZ'], moonDict[3]['pZ'], moonDict[3]['vZ'])
    while(True):
        if t == 1000 and partTwo is False:
            break
        for i in range(len(moonDict.keys()) - 1):
            for j in range(i + 1, len(moonDict.keys())):
                if moonDict[i]['pZ'] < moonDict[j]['pZ']:
                    moonDict[i]['vZ'] += 1
                    moonDict[j]['vZ'] -= 1
                elif moonDict[i]['pZ'] > moonDict[j]['pZ']:
                    moonDict[i]['vZ'] -= 1
                    moonDict[j]['vZ'] += 1
        for moon in moonDict.keys():
            moonDict[moon]['pZ'] += moonDict[moon]['vZ']
        zState = (moonDict[0]['pZ'], moonDict[0]['vZ'], moonDict[1]['pZ'], moonDict[1]['vZ'], moonDict[2]['pZ'], moonDict[2]['vZ'], moonDict[3]['pZ'], moonDict[3]['vZ'])
        if partTwo is True and zState == zOrig:
            zCycleLength = t + 1
            break
        else:
            t += 1
    if partTwo is False:
        return(sum([(abs(moonDict[moon]['pX']) + abs(moonDict[moon]['pY']) + abs(moonDict[moon]['pZ'])) * (abs(moonDict[moon]['vX']) + abs(moonDict[moon]['vY']) + abs(moonDict[moon]['vZ'])) for moon in moonDict.keys()]))
    else:
        return(math.lcm(xCycleLength, yCycleLength, zCycleLength))

analyzeOrbits(moons)

# part 2
analyzeOrbits(moons, True)