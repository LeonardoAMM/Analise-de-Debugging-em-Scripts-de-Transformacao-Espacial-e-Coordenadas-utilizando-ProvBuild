import math
import pandas as pd
from transformations import convert_coordinates
from visualization import *


def calculate_distance(x1, y1, x2, y2):

    distance = math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

    return distance

def is_inside_radius(distance, radius):
    return distance <= radius

def read_data(pd):

    # Lê o arquivo CSV contendo os hospitais
    hospitals = pd.read_csv("data/hospitals.csv")

    # Lê o arquivo CSV contendo os pontos
    points = pd.read_csv("data/points.csv")

    return hospitals, points

def store_data(hospitals, points):

    # Cria listas vazias para armazenar as coordenadas UTM dos hospitais
    hospital_x = []
    hospital_y = []


    # Percorre cada hospital do DataFrame
    for index, row in hospitals.iterrows():

        # Converte latitude/longitude para coordenadas UTM
        x, y = convert_coordinates(
            row["latitude"],
            row["longitude"]
        )

        # Armazena as coordenadas convertidas nas listas
        hospital_x.append(x)
        hospital_y.append(y)


    # Adiciona as coordenadas UTM como novas colunas no DataFrame de hospitais
    hospitals["x"] = hospital_x
    hospitals["y"] = hospital_y


    # Cria listas vazias para armazenar as coordenadas UTM dos pontos
    point_x = []
    point_y = []


    # Percorre cada ponto do DataFrame
    for index, row in points.iterrows():

        # Converte latitude/longitude para coordenadas UTM
        x, y = convert_coordinates(
            row["latitude"],
            row["longitude"]
        )

        # Armazena as coordenadas convertidas nas listas
        point_x.append(x)
        point_y.append(y)



    # Adiciona as coordenadas UTM como novas colunas no DataFrame de pontos
    points["x"] = point_x
    points["y"] = point_y