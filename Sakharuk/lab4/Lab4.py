import matplotlib.pyplot as plt
import numpy as np

x0 = 0.1
t = 60
r_exp = [0.1, 0.3, 0.6, 0.9, 1.0, 1.18, 1.2, 1.22]

# ЭКСПОНЕНЦИАЛЬНЫЙ РОСТ
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

for j in range(4):
    x_ar = [0] * (t + 1)
    x_ar[0] = x0
    
    for i in range(1, t + 1):
        x_ar[i] = r_exp[j] * x_ar[i - 1]
    
    axes[0].plot(range(t + 1), x_ar, label=f'r = {r_exp[j]}')

axes[0].set_xlabel('Время (t)')
axes[0].set_ylabel('x(t)')
axes[0].set_title('Экспоненциальный рост (r < 1)')
axes[0].legend()
axes[0].grid(True)

for j in range(4, len(r_exp)): 
    x_ar = [0] * (t + 1)
    x_ar[0] = x0
    
    for i in range(1, t + 1):
        x_ar[i] = r_exp[j] * x_ar[i - 1]
    
    axes[1].plot(x_ar, label=f'r = {r_exp[j]}')

axes[1].set_xlabel('Время (t)')
axes[1].set_ylabel('x(t)')
axes[1].set_title('Экспоненциальный рост (r ≥ 1)')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()

# ЛОГИСТИЧЕСКАЯ МОДЕЛЬ 
r_log = [1.0, 2.0, 2.3, 2.6, 2.9, 3.3, 3.6, 3.8, 4]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

for j in range(5):
    x_ar = [0] * (t + 1)
    x_ar[0] = x0
    
    for i in range(1, t + 1):
        x_ar[i] = r_log[j] * x_ar[i - 1] * (1 - x_ar[i - 1])
    
    axes[0, 0].plot(range(t + 1), x_ar, label=f'r = {r_log[j]}')

axes[0, 0].set_xlabel('Время (t)')
axes[0, 0].set_ylabel('x(t)')
axes[0, 0].set_title('Логистическая: стабильные (r ≤ 2.9)')
axes[0, 0].legend()
axes[0, 0].grid(True)

for j in range(5, 7): 
    x_ar = [0] * (t + 1)
    x_ar[0] = x0
    
    for i in range(1, t + 1):
        x_ar[i] = r_log[j] * x_ar[i - 1] * (1 - x_ar[i - 1])
    
    axes[0, 1].plot(range(t + 1), x_ar, label=f'r = {r_log[j]}')

axes[0, 1].set_xlabel('Время (t)')
axes[0, 1].set_ylabel('x(t)')
axes[0, 1].set_title('Логистическая: колебания (r > 3.0)')
axes[0, 1].legend()
axes[0, 1].grid(True)

for j in range(7, len(r_log)): 
    x_ar = [0] * (t + 1)
    x_ar[0] = x0
    
    for i in range(1, t + 1):
        x_ar[i] = r_log[j] * x_ar[i - 1] * (1 - x_ar[i - 1])
    
    axes[1, 0].plot(range(t + 1), x_ar, label=f'r = {r_log[j]}')

axes[1, 0].set_xlabel('Время (t)')
axes[1, 0].set_ylabel('x(t)')
axes[1, 0].set_title('Логистическая: хаос (r > 3.6)')
axes[1, 0].legend()
axes[1, 0].grid(True)

r_values_log = np.linspace(2.5, 4.0, 10000)
n_iter = 1000
last = 100
x = 0.1 * np.ones_like(r_values_log)

for i in range(n_iter):
    x = r_values_log * x * (1 - x)
    if i >= (n_iter - last):
        axes[1, 1].plot(r_values_log, x, ',k', alpha=0.05, markersize=0.5)

axes[1, 1].set_xlabel('Параметр r')
axes[1, 1].set_ylabel('Установившееся x(t)')
axes[1, 1].set_title('Бифуркационная диаграмма логистической')
axes[1, 1].grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# МОДЕЛЬ МОРАНА
r_moran = [1.1, 1.3, 1.5, 2.0, 2.2, 2.4, 2.6, 2.9, 3.3]

fig, axes = plt.subplots(2, 2, figsize=(16, 12)) 

for j in range(3): 
    x_ar = [0] * (t + 1)
    x_ar[0] = x0
    
    for i in range(1, t + 1):
        x_ar[i] = x_ar[i - 1] * np.exp(r_moran[j] * (1 - x_ar[i - 1]))
    
    axes[0, 0].plot(range(t + 1), x_ar, label=f'r = {r_moran[j]}')

axes[0, 0].set_xlabel('Время (t)')
axes[0, 0].set_ylabel('x(t)')
axes[0, 0].set_title('Модель Морана: стабильные (r ≤ 1.5)')
axes[0, 0].legend()
axes[0, 0].grid(True)

for j in range(3, 6):
    x_ar = [0] * (t + 1)
    x_ar[0] = x0
    
    for i in range(1, t + 1):
        x_ar[i] = x_ar[i - 1] * np.exp(r_moran[j] * (1 - x_ar[i - 1]))
    
    axes[0, 1].plot(range(t + 1), x_ar, label=f'r = {r_moran[j]}')

axes[0, 1].set_xlabel('Время (t)')
axes[0, 1].set_ylabel('x(t)')
axes[0, 1].set_title('Модель Морана: колебания (r = 2.0-2.4)')
axes[0, 1].legend()
axes[0, 1].grid(True)

for j in range(6, len(r_moran)): 
    x_ar = [0] * (t + 1)
    x_ar[0] = x0
    
    for i in range(1, t + 1):
        x_ar[i] = x_ar[i - 1] * np.exp(r_moran[j] * (1 - x_ar[i - 1]))
    
    axes[1, 0].plot(range(t + 1), x_ar, label=f'r = {r_moran[j]}')

axes[1, 0].set_xlabel('Время (t)')
axes[1, 0].set_ylabel('x(t)')
axes[1, 0].set_title('Модель Морана: хаос (r > 2.6)')
axes[1, 0].legend()
axes[1, 0].grid(True)

# График 4: Бифуркационная диаграмма Морана
r_values_moran = np.linspace(1.0, 4.0, 10000)
n_iter = 1000
last = 100
x = 0.1 * np.ones_like(r_values_moran)

for i in range(n_iter):
    x = x * np.exp(r_values_moran * (1 - x))
    if i >= (n_iter - last):
        axes[1, 1].plot(r_values_moran, x, ',k', alpha=0.05, markersize=0.5)

axes[1, 1].set_xlabel('Параметр r')
axes[1, 1].set_ylabel('Установившееся x(t)')
axes[1, 1].set_title('Бифуркационная диаграмма модели Морана')
axes[1, 1].grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# МОДЕЛЬ ХОЗЯИН-ПАРАЗИТ с фиксированными параметрами
x0_host = 20  
y0_parasite = 5   

a = 0.1  
b = 1.2  
c = 1.0 

fig, ax = plt.subplots(figsize=(12, 8))

x_ar = [0] * (t + 1)
y_ar = [0] * (t + 1)
x_ar[0] = x0_host
y_ar[0] = y0_parasite

for i in range(1, t + 1):
    exp_term = np.exp(-a * y_ar[i - 1])
    x_ar[i] = b * x_ar[i - 1] * exp_term
    y_ar[i] = c * x_ar[i - 1] * (1 - exp_term)

time = range(t + 1)
ax.plot(time, x_ar, 'b-', linewidth=2, label='Хозяева (x_t)')
ax.plot(time, y_ar, 'r-', linewidth=2, label='Паразиты (y_t)')
ax.set_xlabel('Время (t)', fontsize=12)
ax.set_ylabel('Популяция', fontsize=12)
ax.set_title(f'Модель "Хозяин-Паразит" Николсона-Бейли\n(a={a}, b={b}, c={c})', fontsize=14)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()