import pandas as pd
from transformations import convert_coordinates
from general_functions import *
from visualization import *

BUFFER_RADIUS = 2

# Lê arquivos CSV
hospitals, points = read_data(pd)

# Armazena coordenadas de cada ponto e hospital, já convertidas
store_data(hospitals, points)

# Raio em quilômetros
radius_km = BUFFER_RADIUS

# Conversão para metros
radius_m = radius_km * 1000

selected_points = []
all_points = []
all_hospitals = []

# Armazena os pontos sem cobertura em selected_points
for _, point in points.iterrows():
    
    covered = False

    for _, hospital in hospitals.iterrows():

        distance = calculate_distance(hospital["x"], hospital["y"], point["x"], point["y"])
        

        if is_inside_radius(distance, radius_m):
            covered = True
            break
        
    if not covered:
        selected_points.append(point)

selected_points = pd.DataFrame(selected_points)

fig, ax = create_plot()

plot_hospitals(ax, hospitals)
plot_task2(ax, hospitals, points, selected_points)

plt.show()