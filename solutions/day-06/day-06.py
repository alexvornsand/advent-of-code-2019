# advent of code 2019
# day 6

# part 1
orbits = open('input.txt', 'r').read().split('\n')[:-1]

def countOrbits(orbits, partTwo=False):
    def listOrbits(orbits, node, lineage):
        orbitsList = []
        currentNode = node if lineage == '' else lineage + ')' + node
        for orbit in [o for o in orbits if o.split(')')[0] == node]:
            orbitee = orbit.split(')')[1]
            orbitsList.append(currentNode + ')' + orbitee)
            orbitsList += (listOrbits(orbits, orbitee, currentNode))
        return(orbitsList)
    orbitsList = listOrbits(orbits, 'COM', '')
    if partTwo is False:
        return(sum([len(x.split(')')[:-1]) for x in orbitsList]))
    else:
        me = [o for o in orbitsList if o.split(')')[-1] == 'YOU'][0].split(')')[:-1]
        santa = [o for o in orbitsList if o.split(')')[-1] == 'SAN'][0].split(')')[:-1]
        onlyMe = len([o for o in me if o not in santa])
        onlySanta = len([o for o in santa if o not in me])
        return(onlyMe + onlySanta)

countOrbits(orbits)

# part 2
countOrbits(orbits, True)
