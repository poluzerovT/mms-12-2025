import math
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Tuple, List, Any, Dict

PLOT_DIR = "Korzun/lab4_plots"
REPORT_PATH = "Korzun/lab4_report.md"

def exponential_model(r: float) -> Callable[[float], float]:
    return lambda x: r * x

def logistic_model(r: float) -> Callable[[float], float]:
    return lambda x: r * x * (1 - x)

def moran_model(r: float) -> Callable[[float], float]:
    return lambda x: x * math.exp(r * (1 - x))

def nicholson_bailey_model(b: float, a: float, c: float) -> Callable[[float, float], Tuple[float, float]]:
    def step(x: float, y: float) -> Tuple[float, float]:
        try:
            exp_term = math.exp(-a * y)
            x_next = b * x * exp_term
            y_next = c * x * (1 - exp_term)
            return x_next, y_next
        except OverflowError:
            return float('inf'), float('inf')
    return step

def simulate_1d(model_func: Callable[[float], float], x0: float, steps: int) -> List[float]:
    trajectory = [x0]
    x = x0
    for _ in range(steps):
        try:
            x = model_func(x)
        except (OverflowError, ValueError):
            x = float('inf')
        trajectory.append(x)
        if math.isinf(x) or math.isnan(x):
            break
    return trajectory

def simulate_2d(model_func: Callable[[float, float], Tuple[float, float]], x0: float, y0: float, steps: int) -> Tuple[List[float], List[float]]:
    traj_x = [x0]
    traj_y = [y0]
    x, y = x0, y0
    for _ in range(steps):
        try:
            x, y = model_func(x, y)
        except (OverflowError, ValueError):
            x, y = float('inf'), float('inf')
        traj_x.append(x)
        traj_y.append(y)
        if math.isinf(x) or math.isnan(x) or math.isinf(y) or math.isnan(y):
            break
    return traj_x, traj_y

def plot_trajectories(trajectories: List[Tuple[List[float], str]], title: str, filename: str, ylabel: str = "x"):
    plt.figure(figsize=(10, 6))
    for traj, label in trajectories:
        plt.plot(traj, marker='.', linestyle='-', markersize=2, label=label, alpha=0.7)
    plt.title(title)
    plt.xlabel("t")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, alpha=0.3)
    filepath = os.path.join(PLOT_DIR, filename)
    plt.savefig(filepath)
    plt.close()
    return filename

def plot_phase_2d(traj_x: List[float], traj_y: List[float], title: str, filename: str):
    plt.figure(figsize=(8, 8))
    plt.plot(traj_x, traj_y, marker='.', linestyle='-', markersize=2, alpha=0.6)
    plt.title(title)
    plt.xlabel("Хозяин (x)")
    plt.ylabel("Паразит (y)")
    plt.grid(True, alpha=0.3)
    filepath = os.path.join(PLOT_DIR, filename)
    plt.savefig(filepath)
    plt.close()
    return filename

def plot_bifurcation(model_factory: Callable[[float], Callable], r_min: float, r_max: float, steps: int = 500, transient: int = 200, resolution: int = 500, title: str = "Bifurcation", filename: str = "bifurcation.png"):
    r_values = np.linspace(r_min, r_max, resolution)
    x_final = []
    r_points = []
    x0 = 0.5 
    
    for r in r_values:
        model = model_factory(r)
        x = x0
        for _ in range(transient):
            try:
                x = model(x)
            except (OverflowError, ValueError):
                x = float('nan')
                break
        
        if not math.isnan(x) and not math.isinf(x):
            for _ in range(steps):
                try:
                    x = model(x)
                except (OverflowError, ValueError):
                    break
                x_final.append(x)
                r_points.append(r)

    plt.figure(figsize=(12, 8))
    plt.scatter(r_points, x_final, s=0.1, color='black', alpha=0.5)
    plt.title(title)
    plt.xlabel("Параметр r")
    plt.ylabel("Популяция x")
    plt.grid(True, alpha=0.3)
    filepath = os.path.join(PLOT_DIR, filename)
    plt.savefig(filepath)
    plt.close()
    return filename

def run_task_1_2(results):
    r_stable = 2.5
    traj1 = simulate_1d(logistic_model(r_stable), x0=0.1, steps=50)
    traj2 = simulate_1d(logistic_model(r_stable), x0=0.6, steps=50)
    fn1 = plot_trajectories([(traj1, "x0=0.1"), (traj2, "x0=0.6")], 
                            f"Логистическая (r={r_stable}): Сходимость с разных x0", "log_stable_x0.png")
    
    r_chaos = 3.9
    traj3 = simulate_1d(logistic_model(r_chaos), x0=0.10000, steps=50)
    traj4 = simulate_1d(logistic_model(r_chaos), x0=0.10001, steps=50)
    fn2 = plot_trajectories([(traj3, "x0=0.10000"), (traj4, "x0=0.10001")], 
                            f"Логистическая (r={r_chaos}): Чувствительность к x0", "log_chaos_x0.png")

    results["Задание 1-2: Влияние x0 и параметров (Логистическая)"] = [
        {"desc": f"При r={r_stable} траектории ведут себя схоже и сходятся к одной точке независимо от старта.", "img": fn1},
        {"desc": f"При r={r_chaos} (хаос) поведение траекторий существенно отличается даже при минимальном изменении x0.", "img": fn2}
    ]

    traj_exp1 = simulate_1d(exponential_model(1.1), x0=1.0, steps=20)
    traj_exp2 = simulate_1d(exponential_model(0.9), x0=10.0, steps=20)
    fn_exp = plot_trajectories([(traj_exp1, "r=1.1 (рост)"), (traj_exp2, "r=0.9 (вымирание)")],
                               "Экспоненциальная модель", "exponential.png")
    results["Экспоненциальная модель"] = [{"desc": "При r > 1 бесконечный рост, при r < 1 вымирание.", "img": fn_exp}]


def run_task_3(results):
    fn_log_bif = plot_bifurcation(logistic_model, 2.5, 4.0, title="Логистическая: Бифуркационная диаграмма", filename="log_bifurcation.png")
    
    fn_moran_bif = plot_bifurcation(moran_model, 1.0, 4.0, title="Модель Морана: Бифуркационная диаграмма", filename="moran_bifurcation.png")
    
    results["Задание 3: Качественное изменение (Бифуркации)"] = [
        {"desc": "Логистическая модель: видно изменение поведения (точка -> 2-цикл -> 4-цикл -> хаос) при увеличении r.", "img": fn_log_bif},
        {"desc": "Модель Морана: аналогичный каскад бифуркаций при изменении параметра r.", "img": fn_moran_bif}
    ]

def run_host_parasite(results):
    b, a, c = 2.0, 0.1, 1.0
    tx, ty = simulate_2d(nicholson_bailey_model(b, a, c), 10.0, 10.0, 100)
    fn_hp = plot_trajectories([(tx, "Хозяин"), (ty, "Паразит")], f"Хозяин-Паразит (b={b}, a={a}, c={c})", "host_parasite_time.png")
    fn_hp_phase = plot_phase_2d(tx, ty, "Фазовый портрет", "host_parasite_phase.png")
    
    results["Модель Хозяин-Паразит"] = [
        {"desc": "Траектории во времени (колебательный рост)", "img": fn_hp},
        {"desc": "Фазовый портрет (раскручивающаяся спираль - неустойчивость)", "img": fn_hp_phase}
    ]

def main():
    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)
    
    results = {}
    
    print("Выполнение Задания 1 и 2...")
    run_task_1_2(results)
    
    print("Выполнение Задания 3...")
    run_task_3(results)
    
    print("Моделирование Хозяин-Паразит...")
    run_host_parasite(results)
    
    print(f"Графики сохранены в директорию: {PLOT_DIR}")

if __name__ == "__main__":
    main()
