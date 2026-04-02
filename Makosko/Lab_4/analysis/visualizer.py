import matplotlib.pyplot as plt
import numpy as np


def plot_trajectory(trajectories, title="Population Dynamics", param_str="", labels=None):
    """
    Строит график численности популяций от времени для нескольких траекторий
    
    trajectories - список траекторий или одна траектория
    title - заголовок графика
    param_str - строка параметров
    labels - подписи для каждой траектории
    """

    if not isinstance(trajectories, (list, tuple)):
        trajectories = [trajectories]
    
    plt.figure(figsize=(12, 6))
    
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    linestyles = ['-', '--', '-.', ':']
    
    for i, trajectory in enumerate(trajectories):
        time = np.arange(len(trajectory))
        
        if labels and i < len(labels):
            label = labels[i]
        else:
            label = f'Model {i+1}'
        
        color = colors[i % len(colors)]
        linestyle = linestyles[i % len(linestyles)]
        
        if trajectory.ndim == 1 or (trajectory.ndim == 2 and trajectory.shape[1] == 1):
            data = trajectory.flatten() if trajectory.ndim == 2 else trajectory
            plt.plot(time, data, label=label, color=color, linestyle=linestyle, linewidth=2)
        
        elif trajectory.ndim == 2 and trajectory.shape[1] >= 2:
            plt.plot(time, trajectory[:, 0], label=f'{label} - Hosts', 
                    color=color, linestyle=linestyle, linewidth=2, alpha=0.8)
            plt.plot(time, trajectory[:, 1], label=f'{label} - Parasitoids', 
                    color=color, linestyle=':', linewidth=2, alpha=0.8)
        
    plt.title(f"{title}\n{param_str}", fontsize=14)
    plt.xlabel('Time steps (t)')
    plt.ylabel('Population Size')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_phase_portrait(trajectory, title="Phase Portrait"):
    """
    Строит фазовый портрет (y от x) для системы Хозяин-Паразит
    """
    if trajectory.ndim == 2 and trajectory.shape[1] >= 2:
        plt.figure(figsize=(6, 6))
        
        plt.plot(trajectory[:, 0], trajectory[:, 1], 'b-', linewidth=1.5)
        
        plt.title(title)
        plt.xlabel('Hosts (x)')
        plt.ylabel('Parasitoids (y)')
        plt.grid(True)
        plt.show()

def plot_bifurcation_diagram(model_class, param_name, param_range, steps=500, last_steps=50, x0=0.5, const_params=None):
    """
    Строит бифуркационную диаграмму.
    Определение значений параметров, где поведение меняется.
    """
    if const_params is None:
        const_params = {}
        
    x_vals = []
    r_vals = []
    
    
    for r in param_range:
        # Обновляем изменяемый параметр
        current_params = const_params.copy()
        current_params[param_name] = r
        
        model = model_class(params=current_params)
        
        try:
            traj = model.simulate(x0, steps)
            steady_state = traj[-last_steps:]
            steady_state = steady_state[np.isfinite(steady_state)]
            
            r_vals.extend([r] * len(steady_state))
            x_vals.extend(steady_state)
        except RuntimeWarning:
            continue

    plt.figure(figsize=(12, 8))
    plt.scatter(r_vals, x_vals, s=0.1, color='black')
    plt.title(f"Bifurcation Diagram: {model_class.__name__} (param: {param_name})")
    plt.xlabel(f"Parameter {param_name}")
    plt.ylabel("Population values (Attractor)")
    plt.show()