import pandas as pd
from transformations import convert_coordinates
from analysis import calculate_distance
from visualization import plot_points


# Lê o arquivo CSV contendo os hospitais
hospitals = pd.read_csv("data/hospitals.csv")

# Lê o arquivo CSV contendo os pontos
points = pd.read_csv("data/points.csv")


# Cria listas vazias para armazenar as coordenadas UTM dos hospitais
hospital_x = []
hospital_y = []

# Inicializa as variaveis que armazenam a quantidade de hospitais e pontos
qntd_hospitais = 0
qntd_pontos = 0


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

    # Contabiliza a quantidade de hospitais
    qntd_hospitais += 1


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

    # Contabiliza a quantidade de pontos
    qntd_pontos += 1


# Adiciona as coordenadas UTM como novas colunas no DataFrame de pontos
points["x"] = point_x
points["y"] = point_y

# Inicializa vetores para armazenar as distancias 
distance_hospitals = []
distance_points = []
distance_values = []

# Para cada hospital, calcula a distância entre todos os pontos usando as coordenadas já convertidas para UTM e as armazena
for i in range(qntd_hospitais):
    hospital = hospitals.loc[i]
    for j in range(qntd_pontos):
        point = points.loc[j]

        distance = calculate_distance(
            hospital["x"],
            hospital["y"],
            point["x"],
            point["y"]
        )
        
        distance_hospitals.append(hospital["name"])
        distance_points.append(point["name"])
        distance_values.append(distance)

distance_dataframe = pd.DataFrame({
    "hospital": distance_hospitals,
    "point": distance_points,
    "distance": distance_values
})

plot_points(hospitals, points, distance_dataframe)