# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""

import os

import pandas as pd
import matplotlib.pyplot as plt


def pregunta_01():
    """
    El archivo `files/input/shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    # Crear la carpeta docs si no existe

    if not os.path.exists("docs"):
        os.makedirs("docs")

    # Leer los datos
    df = pd.read_csv("files/input/shipping-data.csv")

    # Gráfico 1: Cantidad de envíos por Warehouse_block
    plt.figure(figsize=(8, 6))
    df["Warehouse_block"].value_counts().plot.bar(
        title="Shipping per Warehouse",
        xlabel="Warehouse_block",
        ylabel="Record count",
        color="tab:blue",
        fontsize=8,
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("docs/shipping_per_warehouse.png")
    plt.close()

    # Gráfico 2: Modo de envío
    plt.figure(figsize=(8, 6))
    df["Mode_of_Shipment"].value_counts().plot.pie(
        title="Mode of Shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"],
    )
    plt.savefig("docs/mode_of_shipment.png")
    plt.close()

    # Gráfico 3: Calificación promedio del cliente
    plt.figure(figsize=(8, 6))
    rating_df = (
        df[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    rating_df.columns = rating_df.columns.droplevel()
    rating_df = rating_df[["mean", "min", "max"]]
    plt.barh(
        y=rating_df.index.values,
        width=rating_df["max"] - 1,
        left=rating_df["min"],
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )
    colors = [
        "tab:green" if value >= 3.0 else "tab:orange"
        for value in rating_df["mean"].values
    ]
    plt.barh(
        y=rating_df.index.values,
        width=rating_df["mean"] - 1,
        left=rating_df["min"],
        height=0.5,
        color=colors,
        alpha=1.0,
    )
    plt.title("Average Customer Rating")
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig("docs/average_customer_rating.png")
    plt.close()

    # Gráfico 4: Distribución de peso
    plt.figure(figsize=(8, 6))
    plt.hist(
        df["Weight_in_gms"],
        bins=30,
        color="tab:blue",
        alpha=0.7,
        edgecolor="white",
    )
    plt.title("Shipped Weight Distribution")
    plt.xlabel("Weight in gms")
    plt.ylabel("Record count")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig("docs/weight_distribution.png")
    plt.close()

    # Crear el archivo HTML del dashboard
    html_content = """
    <html>
    <head>
        <title>Shipping Data Dashboard Example</title>
    </head>
    <body>
        <h1>Shipping Data Dashboard</h1>
        <h2>Shipping per Warehouse</h2>
        <img src="shipping_per_warehouse.png" alt="Shipping per Warehouse">
        <h2>Mode of Shipment</h2>
        <img src="mode_of_shipment.png" alt="Mode of Shipment">
        <h2>Average Customer Rating</h2>
        <img src="average_customer_rating.png" alt="Average Customer Rating">
        <h2>Weight Distribution</h2>
        <img src="weight_distribution.png" alt="Weight Distribution">
    </body>
    </html>
    """
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
