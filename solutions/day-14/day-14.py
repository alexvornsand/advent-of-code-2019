# advent of code 2019
# day 14

# part 1
import math

reactions = open('input.txt', 'r').read()[:-1].split('\n')

def makeFuel(reactions, partTwo=False):
    reactionsDict = {}
    for reaction in reactions:
        halves = reaction.split(' => ')
        if ' ' in halves[1]:
            qOutput = int(halves[1].split(' ')[0])
            outputMaterial = halves[1].split(' ')[1]
        else:
            qOutput = 1
            outputMaterial = halves[1]
        ingredients = halves[0].split(', ')
        reactionsDict[outputMaterial] = {
            'Q': qOutput,
            'ingredients': ingredients
        }
    requirements = {'FUEL': 1}
    surplus = dict({material: 0 for material in reactionsDict})
    def countMaterials(reactionsDict, requirements, surplus):
        while(all([requirement == 'ORE' for requirement in requirements]) is False):
            requiredMaterials = list(requirements.keys())
            for requirement in requiredMaterials:
                if requirement != 'ORE':
                    q = requirements[requirement]
                    if surplus[requirement] == 0:
                        pass
                    elif surplus[requirement] > q:
                        surplus[requirement] -= q
                        requirements.pop(requirement)
                        continue
                    else:
                        q -= surplus[requirement]
                        surplus[requirement] = 0
                    qBuilt = math.ceil(q / reactionsDict[requirement]['Q'])
                    qSurplus = qBuilt * reactionsDict[requirement]['Q'] - q
                    surplus[requirement] += qSurplus
                    requirements.pop(requirement)
                    for component in reactionsDict[requirement]['ingredients']:
                        qComponent = int(component.split(' ')[0])
                        componentMaterial = component.split(' ')[1]
                        if componentMaterial in requirements.keys():
                            requirements[componentMaterial] += int(qBuilt * qComponent)
                        else:
                            requirements[componentMaterial] = int(qBuilt * qComponent)
        return(requirements['ORE'], surplus)
    makeFuelResults = countMaterials(reactionsDict, requirements, surplus)
    ore = makeFuelResults[0]
    if partTwo is False:
        return(ore)
    else:
        leftoverFuel = 1000000000000
        makeAtLeast = math.floor(leftoverFuel / ore)
        requirements = {'FUEL': makeAtLeast}
        fuel = 0
        while(leftoverFuel > 0 and makeAtLeast > 0):
            fuel += makeAtLeast
            result = countMaterials(reactionsDict, requirements, surplus)
            leftoverFuel -= result[0]
            makeAtLeast = math.floor(leftoverFuel / ore)
            requirements = {'FUEL': makeAtLeast}
            surplus = result[1]
        return(fuel)

makeFuel(reactions)

# part 2
makeFuel(reactions, True)