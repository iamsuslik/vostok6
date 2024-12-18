import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy import constants
import json

json_file = 'flight_data.json'
with open(json_file, 'r') as f:
    data = json.load(f)

# Обработка пустого списка
if not data:
    print("Ошибка: JSON файл пуст.")
    exit()  # Завершаем программу, если файл пуст


times = []
speeds = []

for item in data:
    if len(item) != 2:
        print(f"Ошибка: В списке {item} не 2 элемента. ")
        continue  # Переходим к следующему элементу списка
    try:
        time = float(item[0])
        speed = float(item[1])
        times.append(time)
        speeds.append(speed)
    except ValueError:
        print(f"Ошибка: Не удалось преобразовать данные в числа в строке {item}")
        continue  # Переходим к следующему элементу списка

max_time = 100
times = np.array(times)  # Преобразуем в numpy array для удобства сравнения
speeds = np.array(speeds)
limited_times = times[times <= max_time]
limited_speeds = speeds[:len(limited_times)]
# данные
m0 = 10000  # масса без топлива
M = 270000  # масса с топливом
Cf = 0.5  # сопротивление
ro = 1.293  # плотность воздуха
S = constants.pi * ((2.5 / 2) ** 2)  # площадь сечения
g = 1.00034 * constants.g
F = [4368630, 1107000]
def dv_dt(t, v):
    if t < 30:
        M = 270000
        m0 = 10000
        Ft = F[0]
        k = (M - m0) / (120)
        return ((Ft / (M - k * t)) + ((Cf * ro * S) / (2 * (M - k * t))) * v ** 2 - g)
    if t < 120:
        M = 132000
        m0 = 10000
        Ft = F[1]
        k = (M - m0) / (300)
        return ((Ft / (M - k * t)) + ((Cf * ro * S) / (2 * (M - k * t))) * v ** 2 - g)
v0 = 0

t = np.linspace(0, 150, 150)

solve = integrate.solve_ivp(dv_dt, t_span=(0, max(t)), y0=[v0], t_eval=t)

x = solve.t
y = solve.y[0]

plt.figure(figsize=(8, 8))
plt.plot(x, y, '-r', label="v(t) (физ. модель)")
plt.plot(limited_times, limited_speeds, color='orange', label="v(t) (данные из ksp)")
plt.legend()
plt.title('Скорость от времени')
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.grid(True)
plt.show()
