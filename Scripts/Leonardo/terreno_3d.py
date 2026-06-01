# -*- coding: utf-8 -*-
import math

def calcular_altura_terreno(x, z, amplitude, frequencia):
    """Calcula a altura Y do terreno no espaco 3D usando ondas senoidais."""
    # Calcula a distancia do ponto (x, z) ate o centro (0, 0)
    distancia_centro = math.sqrt(x*x + z*z)
    
    altura_onda = amplitude * math.sin(distancia_centro * frequencia)
    
    ruido_extra = (amplitude / 3.0) * math.cos(x * frequencia) * math.sin(z * frequencia)
    
    return altura_onda + ruido_extra

def projetar_isometrico(x, y, z, escala, tela_centro_x, tela_centro_y):
    # Constantes da projecao isometrica (Angulo de 30 graus)
    cos30 = 0.866025
    sin30 = 0.5
    
    x_projetado = (x - z) * cos30
    
    y_projetado = (x + z) * sin30 - y
    
    x_final = (x_projetado * escala) + tela_centro_x
    y_final = (y_projetado * escala) + tela_centro_y
    
    return [x_final, y_final]

def gerar_cor_por_altura(y_real, amplitude_maxima):
    altura_normalizada = (y_real + amplitude_maxima) / (amplitude_maxima * 2.0)
    
    if altura_normalizada < 0.0: altura_normalizada = 0.0
    if altura_normalizada > 1.0: altura_normalizada = 1.0
    
    r = int(20 + (altura_normalizada * 0))     # Mantem baixo o vermelho
    g = int(50 + (altura_normalizada * 150))   # Aumenta o verde
    b = int(100 + (altura_normalizada * 155))  # Aumenta o azul
    
    cor_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return cor_hex

def desenhar_terreno_svg(poligonos, largura, altura):
    linhas = []
    linhas.append('<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" style="background-color: #0b0c10;">'.format(largura, altura))
    
    for poli in poligonos:
        # Cada poli tem: [p1, p2, p3, p4, cor_preenchimento]
        p1, p2, p3, p4, cor = poli
        pontos_str = "{},{} {},{} {},{} {},{}".format(
            p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p4[0], p4[1]
        )
        elemento = '<polygon points="{}" fill="{}" stroke="#1f2833" stroke-width="0.5" />'.format(pontos_str, cor)
        linhas.append(elemento)
        
    linhas.append('</svg>')
    return "\n".join(linhas)

# ==========================================
# LÓGICA PRINCIPAL
# ==========================================

# Configurações da Câmera e Imagem
RESOLUCAO_X = 1000
RESOLUCAO_Y = 800
ESCALA_ZOOM = 25.0

# Configurações do Espaço Geométrico
TAMANHO_GRADE = 15
AMPLITUDE_ONDA = 4.0      # Altura das montanhas
FREQUENCIA_ONDA = 0.4     # Quantidade de ondulações

# Geração dos Pontos no Espaço 3D
malha_3d = {}
for coord_x in xrange(-TAMANHO_GRADE, TAMANHO_GRADE + 1):
    for coord_z in xrange(-TAMANHO_GRADE, TAMANHO_GRADE + 1):
        coord_y = calcular_altura_terreno(coord_x, coord_z, AMPLITUDE_ONDA, FREQUENCIA_ONDA)
        malha_3d[(coord_x, coord_z)] = coord_y

# Projeção 2D e Criação dos Polígonos (Quadrados da Malha)
lista_poligonos_2d = []

# Iteramos ate TAMANHO_GRADE - 1 para podermos pegar o proximo ponto (+1) e fechar o quadrado
for coord_x in xrange(-TAMANHO_GRADE, TAMANHO_GRADE):
    for coord_z in xrange(-TAMANHO_GRADE, TAMANHO_GRADE):
        
        # Pega as alturas (Y) dos 4 cantos do quadrado no espaco 3D
        y_canto_1 = malha_3d[(coord_x, coord_z)]
        y_canto_2 = malha_3d[(coord_x + 1, coord_z)]
        y_canto_3 = malha_3d[(coord_x + 1, coord_z + 1)]
        y_canto_4 = malha_3d[(coord_x, coord_z + 1)]
        
        # Projeta os 4 cantos para a tela 2D
        ponto_1 = projetar_isometrico(coord_x, y_canto_1, coord_z, ESCALA_ZOOM, RESOLUCAO_X / 2.0, RESOLUCAO_Y / 2.0)
        ponto_2 = projetar_isometrico(coord_x + 1, y_canto_2, coord_z, ESCALA_ZOOM, RESOLUCAO_X / 2.0, RESOLUCAO_Y / 2.0)
        ponto_3 = projetar_isometrico(coord_x + 1, y_canto_3, coord_z + 1, ESCALA_ZOOM, RESOLUCAO_X / 2.0, RESOLUCAO_Y / 2.0)
        ponto_4 = projetar_isometrico(coord_x, y_canto_1, coord_z + 1, ESCALA_ZOOM, RESOLUCAO_X / 2.0, RESOLUCAO_Y / 2.0)
        
        # A cor do polígono será baseada na altura média dos 4 cantos
        altura_media = (y_canto_1 + y_canto_2 + y_canto_3 + y_canto_4) / 4.0
        cor_poligono = gerar_cor_por_altura(altura_media, AMPLITUDE_ONDA)
        
        # Guarda o polígono completo na lista
        dados_poligono = [ponto_1, ponto_2, ponto_3, ponto_4, cor_poligono]
        lista_poligonos_2d.append(dados_poligono)


# Renderização para String
codigo_svg_final = desenhar_terreno_svg(lista_poligonos_2d, RESOLUCAO_X, RESOLUCAO_Y)

# Salvar no pc
arquivo = open("terreno_isometrico.svg", "w")
arquivo.write(codigo_svg_final)
arquivo.close()