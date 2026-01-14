import numpy as np
import matplotlib.pyplot as plt

def exponential_model(r, x0, steps=50):
    x = np.zeros(steps)
    x[0] = x0
    for t in range(steps - 1):
        x[t + 1] = r * x[t]
    return x

def logistic_model(r, x0, steps=50):
    x = np.zeros(steps)
    x[0] = x0
    for t in range(steps-1):
        x[t+1] = r * x[t] * (1 - x[t])
    return x

def moran_model(r, x0, steps=100):
    x = np.zeros(steps)
    x[0] = x0
    for t in range(steps-1):
        x[t+1] = x[t] * np.exp(r * (1 - x[t]))
    return x


def host_parasite_model(a, b, c, x0, y0, steps=100):
    x = np.zeros(steps)  # хозяева
    y = np.zeros(steps)  # паразиты
    x[0] = x0
    y[0] = y0

    for t in range(steps - 1):
        exp_term = np.exp(-a * y[t])
        x[t + 1] = b * x[t] * exp_term
        y[t + 1] = c * x[t] * (1 - exp_term)

    return x, y



fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.set_title('СЛУЧАЙ r < 1: ВЫМИРАНИЕ', fontsize=14, fontweight='bold')
ax1.set_xlabel('Время t')
ax1.set_ylabel('Численность популяции x_t')
ax1.grid(True, alpha=0.3)

# Параметры для r < 1
r_values_decay = [0.1, 0.4, 0.6, 0.8]
x0 = 0.1
steps = 50
colors_decay = ['darkred', 'red', 'orange', 'gold']

for r, color in zip(r_values_decay, colors_decay):
    x = exponential_model(r, x0, steps)
    ax1.plot(x, 'o-', color=color, linewidth=2, markersize=4, label=f'r = {r}')

ax1.axhline(y=x0, color='black', linestyle=':', alpha=0.5, label='Начальное значение')

ax1.legend(loc='upper right')
ax1.set_ylim(0, x0 * 1.1)

ax2.set_title('СЛУЧАЙ r ≥ 1: СТАБИЛЬНОСТЬ И РОСТ', fontsize=14, fontweight='bold')
ax2.set_xlabel('Время t')
ax2.set_ylabel('Численность популяции x_t')
ax2.grid(True, alpha=0.3)

# Параметры для r ≥ 1
r_values_growth = [1.0, 1.2, 1.22, 1.24]
colors_growth = ['green', 'lime', 'blue', 'cyan']
steps_growth = 50

for r, color in zip(r_values_growth, colors_growth):
    x = exponential_model(r, x0, steps_growth)
    ax2.plot(x, 'o-', color=color, linewidth=2, markersize=4, label=f'r = {r}')


ax2.axhline(y=x0, color='black', linestyle=':', alpha=0.5, label='Начальное значение')


ax2.legend(loc='upper left')

plt.tight_layout()
plt.show()



plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
r_values = [0.3, 0.6, 0.9]
colors = ['darkred', 'red', 'orange']
x0 = 0.5

for r, color in zip(r_values, colors):
    x = logistic_model(r, x0, 30)
    plt.plot(x, 'o-', color=color, linewidth=2, markersize=4, label=f'r={r}')

plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
plt.title('ВЫМИРАНИЕ: 0 < r < 1')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(-0.05, 0.55)

plt.subplot(1, 3, 2)
r_values = [1.2, 1.5, 1.8]
colors = ['darkgreen', 'green', 'lime']
x0 = 0.1

for r, color in zip(r_values, colors):
    x = logistic_model(r, x0, 25)
    plt.plot(x, 'o-', color=color, linewidth=2, markersize=4, label=f'r={r}')
    # Равновесное значение
    eq = 1 - 1/r
    plt.axhline(y=eq, color=color, linestyle=':', alpha=0.4)

plt.title('МОНОТОННЫЙ РОСТ: 1 < r < 2')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(0, 0.5)

plt.subplot(1, 3, 3)
r_values = [2.2, 2.5, 2.9]
colors = ['darkblue', 'blue', 'lightblue']
x0 = 0.1

for r, color in zip(r_values, colors):
    x = logistic_model(r, x0, 50)
    plt.plot(x, 'o-', color=color, linewidth=2, markersize=4, label=f'r={r}', alpha=0.8)
    # Равновесное значение
    eq = 1 - 1/r
    plt.axhline(y=eq, color=color, linestyle=':', alpha=0.4)

plt.title('ЗАТУХАЮЩИЕ КОЛЕБАНИЯ: 2 < r < 3')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(0, 0.8)

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))

# 2.1 Цикл периода 2 (3.0 < r < 3.45)
plt.subplot(1, 2, 1)
r = 3.2
x0 = 0.1
x = logistic_model(r, x0, 80)

# Показываем только установившийся режим
plt.plot(x, 'bo-', linewidth=2, markersize=4, alpha=0.8)

plt.title(f'ЦИКЛ ПЕРИОДА 2: r={r}')
plt.xlabel('Время t (установившийся режим)')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)

# 2.2 Цикл периода 4 (3.45 < r < 3.57)
plt.subplot(1, 2, 2)
r = 3.5
x0 = 0.1
x = logistic_model(r, x0, 120)

# Показываем установившийся режим
plt.plot(x, 'go-', linewidth=2, markersize=4, alpha=0.8)

plt.title(f'ЦИКЛ ПЕРИОДА 4: r={r}')
plt.xlabel('Время t (установившийся режим)')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================
# 3. ОДИН ГРАФИК: ХАОТИЧЕСКИЙ РЕЖИМ
# ============================================
plt.figure(figsize=(8, 5))

r = 3.7
x0 = 0.1
x = logistic_model(r, x0, 150)

plt.plot(x, 'k-', linewidth=1, alpha=0.8)
plt.title(f'ХАОТИЧЕСКОЕ ПОВЕДЕНИЕ: r={r}', fontsize=12)
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)
plt.ylim(0, 1)

plt.tight_layout()
plt.show()



# ============================================
# ОКНО 1: r = 1.1, 1.3, 1.5
# ============================================
plt.figure(figsize=(12, 4))

# График 1: r = 1.1
plt.subplot(1, 3, 1)
r = 1.1
x0 = 0.1
x = moran_model(r, x0, 50)

plt.plot(x, 'bo-', linewidth=2, markersize=4, alpha=0.8)
plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)

plt.title(f'МОДЕЛЬ МОРАНА\nr = {r}')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.2)


# График 2: r = 1.3
plt.subplot(1, 3, 2)
r = 1.3
x0 = 0.1
x = moran_model(r, x0, 50)

plt.plot(x, 'go-', linewidth=2, markersize=4, alpha=0.8)
plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)

plt.title(f'МОДЕЛЬ МОРАНА\nr = {r}')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.2)


# График 3: r = 1.5
plt.subplot(1, 3, 3)
r = 1.5
x0 = 0.1
x = moran_model(r, x0, 50)

plt.plot(x, 'ro-', linewidth=2, markersize=4, alpha=0.8)
plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)

plt.title(f'МОДЕЛЬ МОРАНА\nr = {r}')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.2)


plt.tight_layout()
plt.show()

# ============================================
# ОКНО 2: r = 2.0, 2.2, 2.6
# ============================================
plt.figure(figsize=(12, 4))

# График 1: r = 2.0
plt.subplot(1, 3, 1)
r = 2.0
x0 = 0.1
x = moran_model(r, x0, 60)

plt.plot(x, 'bo-', linewidth=2, markersize=4, alpha=0.8)
plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)

plt.title(f'МОДЕЛЬ МОРАНА\nr = {r}')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.4)

# График 2: r = 2.2
plt.subplot(1, 3, 2)
r = 2.2
x0 = 0.1
x = moran_model(r, x0, 80)

plt.plot(x, 'go-', linewidth=2, markersize=4, alpha=0.8)
plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)

plt.title(f'МОДЕЛЬ МОРАНА\nr = {r}')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.6)

# График 3: r = 2.6
plt.subplot(1, 3, 3)
r = 2.6
x0 = 0.1
x = moran_model(r, x0, 100)

plt.plot(x, 'ro-', linewidth=2, markersize=4, alpha=0.8)
plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)

plt.title(f'МОДЕЛЬ МОРАНА\nr = {r}')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)
plt.ylim(0, 2.0)

plt.tight_layout()
plt.show()

# ============================================
# ОКНО 3: r = 2.9, 3.2
# ============================================
plt.figure(figsize=(10, 4))

# График 1: r = 2.9
plt.subplot(1, 2, 1)
r = 3.5
x0 = 0.1
x = moran_model(r, x0, 150)

plt.plot(x, 'bo-', linewidth=2, markersize=3, alpha=0.8)
plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)

plt.title(f'МОДЕЛЬ МОРАНА\nr = {r}')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)

# График 2: r = 3.2
plt.subplot(1, 2, 2)
r = 4
x0 = 0.1
x = moran_model(r, x0, 200)

plt.plot(x, 'go-', linewidth=2, markersize=3, alpha=0.8)
plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)

plt.title(f'МОДЕЛЬ МОРАНА\nr = {r}')
plt.xlabel('Время t')
plt.ylabel('Численность x_t')
plt.grid(True, alpha=0.3)


plt.tight_layout()
plt.show()




plt.figure(figsize=(15, 4))

# График 1: Стабильное сосуществование
plt.subplot(1, 3, 1)
a, b, c = 0.1, 2.0, 0.5
x0, y0 = 10, 5
x, y = host_parasite_model(a, b, c, x0, y0, 50)

plt.plot(x, 'b-', linewidth=2, label='Хозяева')
plt.plot(y, 'r-', linewidth=2, label='Паразиты')

plt.title(f'СТАБИЛЬНОЕ СУЩЕСТВОВАНИЕ\nb={b}, c={c}, a={a}')
plt.xlabel('Время t')
plt.ylabel('Численность')
plt.legend()
plt.grid(True, alpha=0.3)

# График 2: Слабое взаимодействие
plt.subplot(1, 3, 2)
a, b, c = 0.05, 2.0, 0.3
x, y = host_parasite_model(a, b, c, x0, y0, 50)

plt.plot(x, 'b-', linewidth=2, label='Хозяева')
plt.plot(y, 'r-', linewidth=2, label='Паразиты')

plt.title(f'СЛАБОЕ ВЗАИМОДЕЙСТВИЕ\nb={b}, c={c}, a={a}')
plt.xlabel('Время t')
plt.ylabel('Численность')
plt.legend()
plt.grid(True, alpha=0.3)

# График 3: Хозяева доминируют
plt.subplot(1, 3, 3)
a, b, c = 0.2, 2.5, 0.2
x, y = host_parasite_model(a, b, c, x0, y0, 60)

plt.plot(x, 'b-', linewidth=2, label='Хозяева')
plt.plot(y, 'r-', linewidth=2, label='Паразиты')

plt.title(f'ХОЗЯЕВА ДОМИНИРУЮТ\nb={b}, c={c}, a={a}')
plt.xlabel('Время t')
plt.ylabel('Численность')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


print("Бифуркационная диаграмма логистической модели...")

plt.figure(figsize=(10, 6))

# Функция логистической модели
def logistic(r, x):
    return r * x * (1 - x)

# Параметры
r_min, r_max = 2.5, 4.0
r_points = 2000
iterations = 1000
last = 200

r_values = np.linspace(r_min, r_max, r_points)
x = 0.1 * np.ones(r_points)

# Пропускаем переходный процесс
for _ in range(iterations):
    x = logistic(r_values, x)

# Собираем последние точки
for i in range(last):
    x = logistic(r_values, x)
    plt.plot(r_values, x, ',k', alpha=0.05, markersize=0.1)

plt.title('БИФУРКАЦИОННАЯ ДИАГРАММА\nЛогистическая модель', fontsize=14)
plt.xlabel('Параметр роста r')
plt.ylabel('Значения x')
plt.grid(True, alpha=0.2)
plt.xlim(r_min, r_max)
plt.ylim(0, 1)

plt.tight_layout()
plt.show()

print("\nБифуркационная диаграмма модели Морана...")

plt.figure(figsize=(10, 6))

# Функция модели Морана
def moran(r, x):
    return x * np.exp(r * (1 - x))

# Параметры
r_min, r_max = 1.0, 5.0
r_points = 2000
r_values = np.linspace(r_min, r_max, r_points)
x = 0.1 * np.ones(r_points)

# Пропускаем переходный процесс
for _ in range(iterations):
    x = moran(r_values, x)

# Собираем последние точки
for i in range(last):
    x = moran(r_values, x)
    plt.plot(r_values, x, ',k', alpha=0.05, markersize=0.1)

plt.title('БИФУРКАЦИОННАЯ ДИАГРАММА\nМодель Морана', fontsize=14)
plt.xlabel('Параметр роста r')
plt.ylabel('Значения x')
plt.grid(True, alpha=0.2)
plt.xlim(r_min, r_max)
plt.ylim(0, 3)

plt.tight_layout()
plt.show()