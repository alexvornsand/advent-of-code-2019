# advent of code 2019
# day 4

# part 1
import re

pwRange = [int(x) for x in '138307-654504'.split('-')]

def countPasswords(pwRange, partTwo=False):
    validPws = []
    for pw in range(pwRange[0], pwRange[1]):
        if partTwo is False:
            rule1 = any([len(m.group(0)) >= 2 for m in [re.search(str(i) + '+', str(pw)) for i in range(10)] if m is not None])
        else:
            rule1 = any([len(m.group(0)) == 2 for m in [re.search(str(i) + '+', str(pw)) for i in range(10)] if m is not None])
        rule2 = all([int(str(pw)[i]) <= int(str(pw)[i + 1]) for i in range(len(str(pw)) - 1)])
        if rule1 and rule2:
            validPws.append(pw)
    return(len(validPws))    

countPasswords(pwRange)

# part 2
countPasswords(pwRange, True)