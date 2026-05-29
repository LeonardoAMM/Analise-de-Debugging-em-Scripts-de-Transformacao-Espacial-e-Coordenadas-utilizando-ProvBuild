# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt

def vecxmatrix(vector, matrix):
    out = [0] * len(vector)
    for i, j in enumerate(matrix):
        for k, m in enumerate(j):
            out[i] += vector[k] * m
    return out

def shear(vector, angle):
    mat = [
        [1, 1/math.tan(angle)],
        [0, 1]
    ]

    return vecxmatrix(vector, mat)

def rotate(vector, angle):
    mat = [
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
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

rotatedvectors = [None] * 5

angle = math.pi * 2/6

for i in range(5):
    shearedvectors[i] = shear(vectors[i], angle)
    
for i in shearedvectors:
    print(i)

for i in range(5):
    rotatedvectors[i] = rotate(vectors[i], -math.pi/2)
    

for i in rotatedvectors:
    print(i)

#visualização

plt.plot(0, 0, 'ko')

for v in vectors:
    plt.plot(v[0], v[1],'ro') 


for v in shearedvectors:
    plt.plot(v[0], v[1],'bo') 

for v in rotatedvectors:
    plt.plot(v[0], v[1],'go')     


plt.show()