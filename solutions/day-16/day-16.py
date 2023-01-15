# advent of code 2019
# day 16

# part 1
from math import comb
import numpy as np
from itertools import cycle, islice

signal = open('input.txt', 'r').read()[:-1]

def decodeSignal(signal, partTwo=False):
    if partTwo is False:
        pattern = [0, 1, 0, -1]
        digits = [int(d) for d in signal]
        transformationMatrix = np.array([list(islice(cycle([d for p in [[pattern[i]] * (j + 1) for i in range(len(pattern))] for d in p]), len(digits) + 1))[1:] for j in range(len(digits))]).transpose()
        signalVector = np.array(digits)
        for i in range(100):
            signalVector = np.mod(np.abs(signalVector @ transformationMatrix), 10)
        return(int(''.join([str(x) for x in signalVector[:8]])))
    else:
        signal = signal * 10000
        startPos = int(signal[:7])
        endPos = startPos + 8
        answer = ''
        for pos in range(startPos, endPos):
            digit = 0
            for index in range(0, len(signal) - pos):
                coef = comb(99 + index, index)
                digit += coef * int(signal[pos + index])
            answer += str(digit % 10)
        return(int(answer))

decodeSignal(signal)

# part 2
decodeSignal(signal, True)