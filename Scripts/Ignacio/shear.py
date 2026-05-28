# -*- coding: utf-8 -*-
from math import tan, pi
import matplotlib.pyplot as plt

def vecxmatrix(vector, matrix):
    out = [0] * len(vector)
    for i, j in enumerate(matrix):
        for k, m in enumerate(j):
            out[i] += vector[k] * m
    return out

def shear(vector, angle):
    mat = [
        [1, 1/tan(angle)],
        [0, 1]
    ]

    return vecxmatrix(vector, mat)

vectors = [
    [1, 1],
    [1, 3],
    [2, 2],
    [3, 1],
    [3, 3]
]

shearedvectors = [None] * 5

angle = pi * 2/6

for i in range(5):
    shearedvectors[i] = shear(vectors[i], angle)
    
for i in shearedvectors:
    print(i)
