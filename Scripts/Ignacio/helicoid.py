import pygame
import numpy as np
import math
import colorsys
baseline = [[0, 0, 0], [3, 3, 0]]

baselines = [
    [[0, 0, 0], [1, 1, 0]]
    ]

def vecxmat3(vec, mat):
    vout = [0] * 3
    for i in range(3):
        for j in range(3):
            vout[i] += vec[j] * mat[i][j]
    return vout

def generate_helix(line, interval, ang = 0, res=64):
    out_lines = []

        
    for i in range(res):
        rotline = []
        for j in line:
            
            z = interval[0] + float(i)/res * (interval[1] - interval[0])
            matrix = [
                [math.cos(z + ang), -math.sin(z - ang), 0],
                [math.sin(z + ang), math.cos(z + ang), 0],
                [0, 0, 1]
            ]
            p = vecxmat3(j, matrix)
            p[2] = z      
            rotline.append(p)

        out_lines.append(rotline)
    return out_lines

def project_isom(obj):
    yang = 0
    xang = math.pi/4

    proj = (
        (math.cos(yang), math.sin(yang) * math.sin(xang), -math.sin(yang) * math.cos(xang)),
        (0, math.cos(xang), math.sin(xang)),
        (math.sin(yang), -math.sin(xang) * math.cos(yang), math.cos(xang) * math.cos(yang))
    )

    pobj = []
    for line in obj:
        pline = []
        for p in line:
            pp = vecxmat3(p, proj)
            pline.append([pp[0] * 1280/20 + 1280/2, pp[1] * -720/20 + 720/2])
        pobj.append(pline)

    return pobj

hel = generate_helix(baseline, [-10, 10])



projected_hel = project_isom(hel)


pygame.init()
res = (1280, 720)
screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()
running = True
maxfps = 144

helix_res = 64

cols = []
for i in range(helix_res):
    hue = float(i)/helix_res
    rgb = colorsys.hsv_to_rgb(hue, 1, 1)
    c = [255 * rgb[0], 255 * rgb[1], 255 * rgb[2]]
    cols.append(c)

print(len(projected_hel))

angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    for i, line in enumerate(projected_hel):
        
        if(i < len(projected_hel) - 1):
            pygame.draw.polygon(screen, cols[i], [line[0], line[1], projected_hel[i+1][1], projected_hel[i+1][0]])
        pygame.draw.line(screen, 'black', line[0], line[1])
    pygame.display.flip()

    dt = float(clock.tick(maxfps))/1000

    angle += math.pi * dt
    if angle > math.pi * 2:
        angle = 0

    hel = generate_helix(baseline, [-10, 10], ang = angle)
    projected_hel = project_isom(hel)

pygame.quit()