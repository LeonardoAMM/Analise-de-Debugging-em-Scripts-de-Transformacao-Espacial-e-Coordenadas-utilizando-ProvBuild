# -*- coding: utf-8 -*-
import math

def multiplicar_matriz_vetor(matriz, vetor):
    """Multiplica uma matriz 3x3 por um vetor 3D."""
    resultado = [0.0, 0.0, 0.0]
    resultado[0] = matriz[0][0]*vetor[0] + matriz[0][1]*vetor[1] + matriz[0][2]*vetor[2]
    resultado[1] = matriz[1][0]*vetor[0] + matriz[1][1]*vetor[1] + matriz[1][2]*vetor[2]
    resultado[2] = matriz[2][0]*vetor[0] + matriz[2][1]*vetor[1] + matriz[2][2]*vetor[2]
    return resultado

def rotacionar_eixo_x(vetor, angulo_graus):
    rad = angulo_graus * math.pi / 180.0
    c = math.cos(rad)
    s = math.sin(rad)
    matriz_rot_x = [
        [1.0, 0.0, 0.0],
        [0.0, c,   -s],
        [0.0, s,    c]
    ]
    return multiplicar_matriz_vetor(matriz_rot_x, vetor)

def rotacionar_eixo_y(vetor, angulo_graus):
    rad = angulo_graus * math.pi / 180.0
    c = math.cos(rad)
    s = math.sin(rad)
    matriz_rot_y = [
        [c,   0.0,  s],
        [0.0, 1.0, 0.0],
        [-s,  0.0,  c]
    ]
    return multiplicar_matriz_vetor(matriz_rot_y, vetor)

def rotacionar_eixo_z(vetor, angulo_graus):
    rad = angulo_graus * math.pi / 180.0
    c = math.cos(rad)
    s = math.sin(rad)
    matriz_rot_z = [
        [c,  -s,   0.0],
        [s,   c,   0.0],
        [0.0, 0.0, 1.0]
    ]
    return multiplicar_matriz_vetor(matriz_rot_z, vetor)

def aplicar_perspectiva(vetor, distancia_camera, largura_tela, altura_tela):
    """Transforma o espaco 3D para coordenadas 2D de tela."""
    x, y, z = vetor
    
    # Previne divisao por zero
    z_dist = z + distancia_camera
    if z_dist == 0:
        z_dist = 0.001
        
    fator_escala = 300.0 / z_dist
    
    # Coordenadas projetadas e centralizadas na tela
    x_projetado = (y * fator_escala) + (largura_tela / 2.0)
    y_projetado = (y * fator_escala) + (altura_tela / 2.0)
    
    return [x_projetado, y_projetado]

def gerar_codigo_svg(pontos_2d, arestas, largura, altura):
    """Gera uma imagem vetorial desenhando as linhas espaciais."""
    linhas_svg = []
    linhas_svg.append('<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" style="background-color: #1a1a1a;">'.format(largura, altura))
    
    for aresta in arestas:
        indice_inicio = aresta[0]
        indice_fim = aresta[1]
        
        p1 = pontos_2d[indice_inicio]
        p2 = pontos_2d[indice_fim]
        
        linha = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="#00ffcc" stroke-width="2" />'.format(p1[0], p1[1], p2[0], p2[1])
        linhas_svg.append(linha)
        
    for p in pontos_2d:
        circulo = '<circle cx="{}" cy="{}" r="4" fill="#ff0055" />'.format(p[0], p[1])
        linhas_svg.append(circulo)
        
    linhas_svg.append('</svg>')
    return "\n".join(linhas_svg)

# ==========================================
# LÓGICA PRINCIPAL (Raiz do Arquivo para o ProvBuild Ler)
# ==========================================

# 1. Definicao da Geometria do Cubo no Espaco
vertices_base = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
]

arestas_cubo = [
    [0, 1], [1, 2], [2, 3], [3, 0], # Face de tras
    [4, 5], [5, 6], [6, 7], [7, 4], # Face da frente
    [0, 4], [1, 5], [2, 6], [3, 7]  # Conexoes entre faces
]

#Parametros de Transformacao
angulo_x = 45.0
angulo_y = 30.0
angulo_z = 15.0

camera_z = 3.0
resolucao_x = 800
resolucao_y = 600

# Processamento Espacial
vertices_rotacionados = []
for v in vertices_base:
    rot_x = rotacionar_eixo_x(v, angulo_x)
    rot_y = rotacionar_eixo_y(rot_x, angulo_y)
    rot_z = rotacionar_eixo_z(rot_y, angulo_z)
    vertices_rotacionados.append(rot_z)

# Projecao no Plano 2D
pontos_finais_2d = []
for v_rot in vertices_rotacionados:
    p_2d = aplicar_perspectiva(v_rot, camera_z, resolucao_x, resolucao_y)
    pontos_finais_2d.append(p_2d)

# Renderizacao para a variavel final
texto_imagem_vetorial = gerar_codigo_svg(pontos_finais_2d, arestas_cubo, resolucao_x, resolucao_y)


arquivo_saida = open("cubo_renderizado.svg", "w")
arquivo_saida.write(texto_imagem_vetorial)
arquivo_saida.close()

print "Transformacao espacial concluida! Abra o arquivo 'cubo_renderizado.svg' no seu navegador."