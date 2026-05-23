import matplotlib.pyplot as plt


def plot_points(hospitals, points, distance_dataframe):

    # Cria figura com tamanho maior
    fig, ax = plt.subplots(figsize=(12, 10))


    # Plota hospitais
    ax.scatter(
        hospitals["x"] / 1000,
        hospitals["y"] / 1000,
        label="Hospitais"
    )


    # Plota pontos
    ax.scatter(
        points["x"] / 1000,
        points["y"] / 1000,
        label="Pontos"
    )


    # Adiciona nomes dos hospitais
    for _, hospital in hospitals.iterrows():

        ax.text(
            hospital["x"] / 1000,
            hospital["y"] / 1000,
            hospital["name"]
        )


    # Adiciona nomes dos pontos
    for _, point in points.iterrows():

        ax.text(
            point["x"] / 1000,
            point["y"] / 1000,
            point["name"]
        )


    # Desenha linhas e distâncias
    for _, hospital in hospitals.iterrows():

        for _, point in points.iterrows():

            x_values = [
                hospital["x"] / 1000,
                point["x"] / 1000
            ]

            y_values = [
                hospital["y"] / 1000,
                point["y"] / 1000
            ]


            ax.plot(x_values, y_values)


            distance = (
                ((point["x"] - hospital["x"]) ** 2 +
                 (point["y"] - hospital["y"]) ** 2) ** 0.5
            ) / 1000


            middle_x = (x_values[0] + x_values[1]) / 2
            middle_y = (y_values[0] + y_values[1]) / 2


            ax.text(
                middle_x,
                middle_y,
                f"{distance:.2f} km"
            )


    # Configurações do gráfico
    ax.legend()
    ax.set_title("Mapa Espacial")
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")

    table_data = distance_dataframe.copy()

    table_data["distance"] = (
        table_data["distance"] / 1000
    )

    # Cria tabela com os dados
    table_data = table_data.round(2)


    table = plt.table(
        cellText=table_data.values,
        colLabels=table_data.columns,
        loc="bottom",
        cellLoc="center"
    )


    # Ajusta tamanho da tabela
    table.scale(1, 1.5)


    # Ajusta espaço da figura
    plt.subplots_adjust(
        left=0.2,
        bottom=0.35
    )


    # Exibe tudo
    plt.show()