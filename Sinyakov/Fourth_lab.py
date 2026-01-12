import numpy as np
import matplotlib.pyplot as plt

def exponential_growth(x0, r, T):
    x = np.zeros(T)
    x[0] = x0
    for t in range(1, T):
        x[t] = r * x[t-1]
    return x

def logistic_model(x0, r, T):
    x = np.zeros(T)
    x[0] = x0
    for t in range(1, T):
        x[t] = r * x[t-1] * (1 - x[t-1])
    return x

def moran_model(x0, r, T):
    x = np.zeros(T)
    x[0] = x0
    for t in range(1, T):
        x[t] = x[t-1] * np.exp(r * (1 - x[t-1]))
    return x

def nicholson_bailey_model(x0, y0, a, b, c, T):
    x = np.zeros(T)
    y = np.zeros(T)
    x[0] = x0
    y[0] = y0
    for t in range(1, T):
        x[t] = b * x[t-1] * np.exp(-a * y[t-1])
        y[t] = c * x[t-1] * (1 - np.exp(-a * y[t-1]))
    return x, y

T = 100

plt.figure(figsize=(15, 10))
plt.subplot(2, 2, 1)
for r in [0.5, 1.0, 1.5, 2.0]:
    x = exponential_growth(10, r, T)
    plt.plot(x, label=f'r={r}')
plt.title('Экспоненциальный рост: разные r')
plt.legend()

plt.subplot(2, 2, 2)
for x0 in [5, 10, 15, 20]:
    x = exponential_growth(x0, 1.5, T)
    plt.plot(x, label=f'x0={x0}')
plt.title('Экспоненциальный рост: разные начальные условия')
plt.legend()

plt.subplot(2, 2, 3)
for r in [0.1, 0.5, 1.0, 2.0, 3.0]:
    x = exponential_growth(1, r, 20)
    plt.plot(x, label=f'r={r}')
plt.title('Экспоненциальный рост (первые 20 шагов)')
plt.legend()

plt.subplot(2, 2, 4)
x = exponential_growth(10, 1.2, T)
plt.plot(x, 'r-', linewidth=2)
plt.title('Экспоненциальный рост: r=1.2, x0=10')
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 10))
plt.subplot(2, 2, 1)
for r in [2.0, 2.5, 3.0, 3.5, 4.0]:
    x = logistic_model(0.1, r, T)
    plt.plot(x, label=f'r={r}')
plt.title('Логистическая модель: разные r')
plt.legend()

plt.subplot(2, 2, 2)
for x0 in [0.1, 0.3, 0.5, 0.7]:
    x = logistic_model(x0, 3.2, T)
    plt.plot(x, label=f'x0={x0}')
plt.title('Логистическая модель: разные начальные условия')
plt.legend()

plt.subplot(2, 2, 3)
r_critical = [2.8, 3.0, 3.2, 3.5, 3.8, 4.0]
for r in r_critical:
    x = logistic_model(0.1, r, T)
    plt.plot(x, label=f'r={r}')
plt.title('Логистическая модель: критические значения r')
plt.legend()

plt.subplot(2, 2, 4)
x = logistic_model(0.1, 3.57, T)
plt.plot(x, 'r-', linewidth=2)
plt.title('Логистическая модель: хаос (r=3.57)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 10))
plt.subplot(2, 2, 1)
for r in [1.0, 1.5, 2.0, 2.5]:
    x = moran_model(0.5, r, T)
    plt.plot(x, label=f'r={r}')
plt.title('Модель Морана: разные r')
plt.legend()

plt.subplot(2, 2, 2)
for x0 in [0.1, 0.5, 1.0, 2.0]:
    x = moran_model(x0, 2.0, T)
    plt.plot(x, label=f'x0={x0}')
plt.title('Модель Морана: разные начальные условия')
plt.legend()

plt.subplot(2, 2, 3)
for r in [0.5, 1.0, 1.8, 2.2, 2.5]:
    x = moran_model(1.0, r, T)
    plt.plot(x, label=f'r={r}')
plt.title('Модель Морана: широкий диапазон r')
plt.legend()

plt.subplot(2, 2, 4)
x = moran_model(0.5, 2.0, T)
plt.plot(x, 'r-', linewidth=2)
plt.title('Модель Морана: r=2.0, x0=0.5')
plt.tight_layout()
plt.show()

# Модель Николсона-Бейли
plt.figure(figsize=(15, 10))
plt.subplot(2, 2, 1)
a_params = [0.05, 0.1, 0.5, 1]
for a in a_params:
    x, y = nicholson_bailey_model(10, 5, a, 1.5, 0.5, T)
    plt.plot(x, label=f'a={a} (хозяева)')
    plt.plot(y, '--', label=f'a={a} (паразиты)')
plt.title('Николсон-Бейли: параметр a')
plt.legend()
plt.ylim(0, 2000)
plt.xlim(0, 100)

plt.subplot(2, 2, 2)
b_params = [1.2, 1.5, 1.8, 2.0]
for b in b_params:
    x, y = nicholson_bailey_model(10, 5, 0.1, b, 0.5, T)
    plt.plot(x, label=f'b={b} (хозяева)')
    plt.plot(y, '--', label=f'b={b} (паразиты)')
plt.title('Николсон-Бейли: параметр b')
plt.legend()

plt.subplot(2, 2, 3)
c_params = [0.3, 0.5, 0.7, 0.9]
for c in c_params:
    x, y = nicholson_bailey_model(10, 5, 0.1, 1.5, c, T)
    plt.plot(x, label=f'c={c} (хозяева)')
    plt.plot(y, '--', label=f'c={c} (паразиты)')
plt.title('Николсон-Бейли: параметр c')
plt.legend()
plt.ylim(0, 2000)
plt.xlim(0, 100)

plt.subplot(2, 2, 4)
x0_params = [5, 10, 15, 20]
y0_params = [2, 5, 8, 10]
for i in range(len(x0_params)):
    x, y = nicholson_bailey_model(x0_params[i], y0_params[i], 0.1, 1.5, 0.5, T)
    plt.plot(x, label=f'x0={x0_params[i]}, y0={y0_params[i]} (хозяева)')
    plt.plot(y, '--', label=f'x0={x0_params[i]}, y0={y0_params[i]} (паразиты)')
plt.title('Николсон-Бейли: начальные условия')
plt.legend()
plt.ylim(0, 2000)
plt.xlim(0, 100)
plt.tight_layout()

plt.show()
