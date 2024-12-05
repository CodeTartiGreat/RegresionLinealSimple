from io import open

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, root_mean_squared_error

# Definición de variables

graph_title, x_title, y_title = None, None, None

x = list()
y = list()
x_err = list()
y_err = list()

# Almacenar los datos en las variables

with open("datos.txt", "r") as f:
    lines = [line.strip().split("|") for line in f]

    graph_title = lines[0][0].strip()
    x_title = lines[1][0].strip()
    y_title = lines[1][1].strip()
    for i in range(len(lines) - 2):
        all_values = lines[i + 2]
        values_x = [float(n) for n in (all_values[0].strip().split(";"))]
        values_y = [float(n) for n in (all_values[1].strip().split(";"))]

        x = np.append(x, values_x[0])
        x_err = np.append(x_err, values_x[1])

        y = np.append(y, values_y[0])
        y_err = np.append(y_err, values_y[1])


# Modelo de regresión lineal simple


def model(x, m, n):
    return m * x + n


parameters, cov = curve_fit(model, x, y)
m, n = parameters

std_m = np.sqrt(cov[0][0])
std_n = np.sqrt(cov[1][1])

# Imprimir información en la terminal

print(f"Pendiente: {m} +- {std_m}")
print(f"Termino independiente: {n} +- {std_n}")

mse = root_mean_squared_error(y, model(x, m, n))
print(f"Error cuadrático medio: {mse}")

rs = r2_score(y, model(x, m, n))
print(f"R^2: {rs}")

# Mostrar la gráfica

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c="blue", marker="x", label="Datos")
ax.plot(x, model(x, m, n), c="salmon", linewidth=2, label="Modelo de ajuste")

ax.set_facecolor("#EBEBEB")
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

ax.set_title(graph_title, fontsize=16)
ax.set_xlabel(rf"{x_title}")
ax.set_ylabel(rf"{y_title}")
ax.axis(
    (
        min(x) - ((max(x) - min(x)) / 25),
        max(x) + ((max(x) - min(x)) / 25),
        min(y) - ((max(y) - min(y)) / 25),
        max(y) + ((max(y) - min(y)) / 25),
    )
)

ax.grid(which="major", color="white", linewidth=1.2)
ax.grid(which="minor", color="white", linewidth=0.6)

ax.errorbar(x, y, yerr=y_err, xerr=x_err, linestyle="None", ecolor="#404040")

ax.legend(loc=4)
plt.show()
