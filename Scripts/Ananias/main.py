import pandas as pd
from transformations import convert_coordinates
from analysis import *
from visualization import plot_points

# Configuração da análise espacial
POINT_NUM = 1
BUFFER_RADIUS = 3

# Lê o arquivo CSV contendo os hospitais
hospitals = pd.read_csv("data/hospitals.csv")

# Lê o arquivo CSV contendo os pontos
points = pd.read_csv("data/points.csv")


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

# Seleciona o ponto de referência
selected_point = points.loc[POINT_NUM-1]

# Raio em quilômetros
radius_km = BUFFER_RADIUS

# Conversão para metros
radius_m = radius_km * 1000

hospital_names = []
distance_values = []

all_hospitals = []
all_distances = []

for index, hospital in hospitals.iterrows():

    distance = calculate_distance(
        hospital["x"],
        hospital["y"],
        selected_point["x"],
        selected_point["y"]
    )

    all_hospitals.append(hospital["name"])
    all_distances.append(distance)

    if is_inside_radius(distance, radius_km):
        hospital_names.append(hospital["name"])
        distance_values.append(distance)

# DataFrame com todos os hospitais
table_dataframe = pd.DataFrame({
    "hospital": all_hospitals,
    "distance": all_distances
})

# DataFrame apenas com os hospitais encontrados
result_dataframe = pd.DataFrame({
    "hospital": hospital_names,
    "distance": distance_values
})



# Visualização
plot_points(hospitals, selected_point, result_dataframe, table_dataframe, radius_m)
