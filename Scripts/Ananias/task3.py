# -*- coding: utf-8 -*-

import pandas as pd
from transformations import convert_coordinates
from general_functions import *
from visualization import *

BUFFER_RADIUS = 3.5

# Lê arquivos CSV
hospitals, points = read_data(pd)

# Armazena coordenadas convertidas
store_data(hospitals, points)

# Raio em quilômetros
radius_km = BUFFER_RADIUS

# Conversão para metros
radius_m = radius_km * 1000

hospital_names = []
covered_points = []

count = 0
# Conta quantos pontos cada hospital cobre
for _, hospital in hospitals.iterrows():

    for _, point in points.iterrows():

        distance = calculate_distance(hospital["x"], hospital["y"], point["x"], point["y"])

        if is_inside_radius(distance, radius_m):
            count += 1

    hospital_names.append(hospital["name"])
    covered_points.append(count)

# Cria DataFrame do ranking
ranking_dataframe = pd.DataFrame({ "hospital": hospital_names, "covered_points": covered_points})

# Ordena do maior para o menor
ranking_dataframe = ranking_dataframe.sort_values(by="covered_points", ascending=False).reset_index(drop=True)

# Cria gráfico
fig, ax = create_plot()

plot_hospitals(ax, hospitals)
plot_task3(ax, hospitals, points, ranking_dataframe, radius_m)

plt.show()