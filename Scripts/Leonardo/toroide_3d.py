# -*- coding: utf-8 -*-
import math

# ==========================================
# FUNCOES DE MATEMATICA E ESPACO 3D
# ==========================================

def graus_para_radianos(graus):
    """Converte angulos de graus para radianos."""
    return graus * math.pi / 180.0

def calcular_coordenada_toroide(angulo_u, angulo_v, raio_principal, raio_tubo):
    """
    Gera o espaco 3D do Toroide (Donut) usando equacoes parametricas.
    u = angulo ao redor do eixo central (o circulo maior)
    v = angulo ao redor do proprio tubo
    """
    rad_u = graus_para_radianos(angulo_u)
    rad_v = graus_para_radianos(angulo_v)
    
    # Equacoes parametricas do Toroide
    x_3d = (raio_principal + raio_tubo * math.cos(rad_v)) * math.cos(rad_u)
    y_3d = (raio_principal + raio_tubo * math.cos(rad_v)) * math.sin(rad_u)
    z_3d = raio_tubo * math.sin(rad_v)
    
    return [x_3d, y_3d, z_3d]

def aplicar_rotacao_espacial(ponto, ang_x, ang_y, ang_z):
    """Aplica rotacao nos eixos X, Y e Z sucessivamente."""
    x, y, z = ponto
    
    # 1. Rotacao no eixo X
    rad_x = graus_para_radianos(ang_x)
    cos_x, sin_x = math.cos(rad_x), math.sin(rad_x)
    y_rot1 = y * cos_x - z * sin_x
    z_rot1 = y * sin_x + z * cos_x
    
    # 2. Rotacao no eixo Y
    rad_y = graus_para_radianos(ang_y)
    cos_y, sin_y = math.cos(rad_y), math.sin(rad_y)
    x_rot2 = x * cos_y + z_rot1 * sin_y
    z_rot2 = -x * sin_y + z_rot1 * cos_y
    
    # 3. Rotacao no eixo Z
    rad_z = graus_para_radianos(ang_z)
    cos_z, sin_z = math.cos(rad_z), math.sin(rad_z)
    x_rot3 = x_rot2 * cos_z - y_rot1 * sin_z
    y_rot3 = x_rot2 * sin_z + y_rot1 * cos_z
    
    return [x_rot3, y_rot3, z_rot2]

def aplicar_perspectiva_camera(ponto_rotacionado, dist_camera, resolucao_w, resolucao_h, escala_lente):
    """Projeta a coordenada 3D em uma tela 2D plana."""
    x, y, z = ponto_rotacionado
    
    # Calcula a profundidade
    profundidade = z + dist_camera
    if profundidade == 0:
        profundidade = 0.001
        
    fator_divisao = escala_lente / profundidade
    
    # Centraliza na tela
    tela_x = (x * fator_divisao) + (resolucao_w / 2.0)
    tela_y = (y * fator_divisao) + (resolucao_h / 2.0)
    
    return [tela_x, tela_y]

def desenhar_malha_svg(lista_linhas_2d, largura, altura):
    """Gera o texto do arquivo SVG renderizando as linhas de conexao."""
    buffer_texto = []
    buffer_texto.append('<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" style="background-color: #0a0510;">'.format(largura, altura))
    
    for ponto_inicio, ponto_fim in lista_linhas_2d:
        linha_svg = '<line x1="{:.2f}" y1="{:.2f}" x2="{:.2f}" y2="{:.2f}" stroke="#ff00aa" stroke-width="1.5" opacity="0.6"/>'.format(
            ponto_inicio[0], ponto_inicio[1], ponto_fim[0], ponto_fim[1]
        )
        buffer_texto.append(linha_svg)
        
    buffer_texto.append('</svg>')
    return "\n".join(buffer_texto)

# ==========================================
# LÓGICA PRINCIPAL (Raiz do Arquivo)
# ==========================================

LARGURA_TELA = 800
ALTURA_TELA = 800
CAMERA_Z = 60.0
LENTE_ESCALA = 1200.0

RAIO_MAIOR = 10.0  # Tamanho geral do donut
RAIO_MENOR = 4.0   # Grossura do tubo
PASSO_ANGULAR = 15 # De quantos em quantos graus calculamos um ponto (15 gera uma malha detalhada)

ROTACAO_X = 60.0
ROTACAO_Y = 25.0
ROTACAO_Z = 10.0

matriz_pontos_projetados = {}

# 1. Geracao do Espaco 3D e Projecao (Mapeamento duplo de 0 a 360 graus)
for u in xrange(0, 360, PASSO_ANGULAR):
    for v in xrange(0, 360, PASSO_ANGULAR):
        
        # Passo A: Cria a coordenada crua
        coord_crua = calcular_coordenada_toroide(u, v, RAIO_MAIOR, RAIO_MENOR)
        
        # Passo B: Gira no espaco
        coord_girada = aplicar_rotacao_espacial(coord_crua, u, ROTACAO_Y, u)
        
        # Passo C: Amassa para 2D
        coord_projetada = aplicar_perspectiva_camera(coord_girada, CAMERA_Z, LARGURA_TELA, ALTURA_TELA, LENTE_ESCALA)
        
        # Guarda no dicionario para podermos conectar as linhas depois
        matriz_pontos_projetados[(u, v)] = coord_projetada

# 2. Conexao dos Pontos (Criando as Arestas da Malha)
linhas_para_renderizar = []

for u in xrange(0, 360, PASSO_ANGULAR):
    for v in xrange(0, 360, PASSO_ANGULAR):
        
        ponto_atual = matriz_pontos_projetados[(u, v)]
        
        # Calcula qual é o proximo ponto na malha (se chegar a 360, volta pro 0 para fechar o circulo)
        proximo_u = (u + PASSO_ANGULAR) % 360
        proximo_v = (v + PASSO_ANGULAR) % 360
        
        ponto_vizinho_anel = matriz_pontos_projetados[(proximo_u, v)]
        ponto_vizinho_tubo = matriz_pontos_projetados[(u, proximo_v)]
        
        # Adiciona a linha horizontal (anel) e vertical (tubo)
        linhas_para_renderizar.append([ponto_atual, ponto_vizinho_anel])
        linhas_para_renderizar.append([ponto_atual, ponto_vizinho_tubo])

# 3. Renderizacao Final
codigo_imagem_svg = desenhar_malha_svg(linhas_para_renderizar, LARGURA_TELA, ALTURA_TELA)

# 4. Salvar no Pc
arquivo_final = open("toroide_neon.svg", "w")
arquivo_final.write(codigo_imagem_svg)
arquivo_final.close()