import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Patch


def create_plot():
    fig, ax = plt.subplots(figsize=(12, 20))
    return fig, ax

def plot_hospitals(ax, hospitals):

    # Plota todos os hospitais
    ax.scatter(hospitals["x"] / 1000, hospitals["y"] / 1000,label="Hospitais")


    # Escreve o nome dos hospitais
    for _, hospital in hospitals.iterrows():

        ax.text(hospital["x"] / 1000 + 0.1, hospital["y"] / 1000 + 0.1, hospital["name"])


def plot_task1(ax, hospitals, selected_point, result_dataframe, table_dataframe, radius_m):

    # Plota o ponto selecionado
    ax.scatter(selected_point["x"] / 1000, selected_point["y"] / 1000, label=selected_point["name"])

    # Nome do ponto
    ax.text(selected_point["x"] / 1000 + 0.1, selected_point["y"] / 1000 + 0.1, selected_point["name"])

    # Desenha círculo de busca
    circle = Circle((selected_point["x"] / 1000, selected_point["y"] / 1000), radius_m / 1000, fill=False)

    ax.add_patch(circle)

    # Desenha linhas apenas para hospitais encontrados
    for _, result in result_dataframe.iterrows():

        hospital_name = result["hospital"]

        hospital = hospitals[hospitals["name"] == hospital_name].iloc[0]

        x_values = [selected_point["x"] / 1000, hospital["x"] / 1000]

        y_values = [selected_point["y"] / 1000, hospital["y"] / 1000]

        ax.plot(x_values, y_values)

        # Texto da distância
        middle_x = (x_values[0] + x_values[1]) / 2
        middle_y = (y_values[0] + y_values[1]) / 2

        ax.text(middle_x, middle_y + 0.15, f"{result['distance']/1000:.2f} km")

    # Configurações do gráfico
    ax.set_title(f"Hospitais em um raio de {radius_m/1000:.1f} km")

    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.legend()

    # Tabela
    table_data = table_dataframe.copy()

    table_data["distance"] = (table_data["distance"] / 1000)

    table_data = table_data.round(2)

    table_data.columns = ["Hospital", "Distância (km)"]

    table = plt.table(cellText=table_data.values, colLabels=table_data.columns, loc="bottom", cellLoc="center", bbox=[0.0, -0.55, 1.0, 0.35])

    table.scale(1, 2.2)
    
    table[0,0].set_facecolor("orange")
    table[0,1].set_facecolor("orange")

    # Destacar em verde os hospitais que estão dentro do raio do buffer
    inside_radius = set(result_dataframe["hospital"])
    
    for row_index, row in table_data.iterrows():
        hospital_name = row["Hospital"]
        if hospital_name in inside_radius:
            for col_index in range(len(table_data.columns)):
                table[(row_index + 1, col_index)].set_facecolor("green")
        else:
            for col_index in range(len(table_data.columns)):
                table[(row_index + 1, col_index)].set_facecolor("red")

    plt.subplots_adjust(
        left=0.15,
        bottom=0.4
    )

    legend_elements = [
    Patch(
        facecolor="green",
        edgecolor="black",
        label="Hospital dentro do raio"
    ),
    Patch(
        facecolor="red",
        edgecolor="black",
        label="Hospital fora do raio"
    )
    ]

    ax.legend(
        handles=legend_elements,
        loc="upper left",
        bbox_to_anchor=(-0.01, -0.15)
    )

def plot_task2(ax, hospitals, points, selected_points):

    ax.scatter(
    points["x"] / 100,
    points["y"] / 100,
    label="Pontos"
    )

    for _, point in points.iterrows():
        ax.text(
            point["x"] / 100 + 0.1,
            point["y"] / 100 + 0.1,
            point["name"]
        )
    
    ax.scatter(
    selected_points["x"] / 100,
    selected_points["y"] / 100,
    color="red",
    marker="x",
    s=120,
    label="Sem cobertura"
    )

    ax.set_title("Pontos sem cobertura hospitalar")
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.legend()

    table_data = selected_points[["name"]].copy()

    table_data.columns = ["Pontos sem cobertura"]

    table = plt.table(
    cellText=table_data.values,
    colLabels=table_data.columns,
    loc="bottom",
    cellLoc="center",
    bbox=[0.0, -0.35, 1.0, 0.20]
    )

    table.scale(1, 2.2)
    table[(0,0)].set_facecolor("orange")

    for i in range(len(table_data)):
        table[(i+1,0)].set_facecolor("red")

    plt.subplots_adjust(
        left=0.15,
        bottom=0.35
    )

    legend_elements = [
        Patch(
             facecolor="red",
             edgecolor="black",
             label="Ponto sem cobertura"
        )
    ]

    ax.legend(
        handles=legend_elements,
        loc="upper left",
        bbox_to_anchor=(-0.01, -0.12)
    )


def plot_task3(ax, hospitals, points, ranking_dataframe, radius_m):

    # Plota todos os pontos
    ax.scatter(
        points["x"] / 1000,
        points["y"] / 1000,
        label="Pontos"
    )

    # Nome dos pontos
    for _, point in points.iterrows():

        ax.text(
            point["x"] / 1000 + 0.1,
            point["y"] / 1000 + 0.1,
            point["name"]
        )

    # Hospitais do Top 3
    top3 = set(
        ranking_dataframe.head(3)["hospital"]
    )

    # Plota hospitais
    for _, hospital in hospitals.iterrows():

        if hospital["name"] in top3:

            ax.scatter(
                hospital["x"] / 1000,
                hospital["y"] / 1000,
                color="green",
                s=120
            )

            # Desenha o buffer do hospital
            circle = Circle(
                (
                    hospital["x"] / 1000,
                    hospital["y"] / 1000
                ),
                radius_m / 1000,
                fill=False,
                color="green",
                linewidth=2,
                linestyle="--"
            )

            ax.add_patch(circle)

        else:

            ax.scatter(
                hospital["x"] / 1000,
                hospital["y"] / 1000
            )

        ax.text(
            hospital["x"] / 1000 + 0.1,
            hospital["y"] / 1000 + 0.1,
            hospital["name"]
        )

    # Configuração do gráfico
    ax.set_title("Ranking de cobertura dos hospitais")

    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")

    # ---------- Tabela ----------

    table_data = ranking_dataframe.head(5).copy()

    table_data.columns = [
        "Hospital",
        "Pontos cobertos"
    ]

    table = plt.table(
        cellText=table_data.values,
        colLabels=table_data.columns,
        loc="bottom",
        cellLoc="center",
        bbox=[0.0, -0.55, 1.0, 0.35]
    )

    table.scale(1, 1.5)

    table[(0,0)].set_facecolor("orange")
    table[(0,1)].set_facecolor("orange")

    # Destaca os três primeiros do ranking
    for row in range(min(3, len(table_data))):

        table[(row + 1, 0)].set_facecolor("green")
        table[(row + 1, 1)].set_facecolor("green")

    plt.subplots_adjust(
        left=0.15,
        bottom=0.45
    )

    legend_elements = [

        Patch(
            facecolor="green",
            edgecolor="black",
            label="Top 3 hospitais"
        )

    ]

    ax.legend(
        handles=legend_elements,
        loc="upper left",
        bbox_to_anchor=(-0.01, -0.15)
    )






########################################################################################


