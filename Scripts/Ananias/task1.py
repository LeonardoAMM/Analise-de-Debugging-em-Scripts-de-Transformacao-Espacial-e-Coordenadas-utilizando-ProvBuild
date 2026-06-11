import pandas as pd
from transformations import convert_coordinates
from general_functions import *
from visualization import *

# Configuração da análise espacial
POINT_NUM = 1
BUFFER_RADIUS = 3

# Lê arquivos CSV
hospitals, points = read_data(pd)

# Armazena coordenadas de cada ponto e hospital, já convertidas
store_data(hospitals, points)

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
fig, ax = create_plot()

plot_hospitals(ax, hospitals)

plot_task1(
    ax,
    hospitals,
    selected_point,
    result_dataframe,
    table_dataframe,
    radius_m
)

plt.show()
