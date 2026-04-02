import numpy as np
from abc import ABC, abstractmethod

class DiscreteModel(ABC):
    """
    Базовый класс для дискретных динамических систем.
    Описывает соотношение x(t+1) = f(x(t)).
    """
    def __init__(self, params: dict):
        self.params = params
        self.trajectory = []

    @abstractmethod
    def step(self, state):
        """
        Вычисляет следующее состояние системы на основе текущего.
        Должен быть переопределен в дочерних классах.
        """
        pass

    def simulate(self, initial_state, steps: int):
        """
        Запускает симуляцию на steps шагов.
        Возвращает массив состояний (траекторию).
        """
        self.trajectory = [initial_state]
        current_state = initial_state
        
        for _ in range(steps):
            if isinstance(current_state, (list, tuple)):
                current_state = np.array(current_state)
            
            next_state = self.step(current_state)
            self.trajectory.append(next_state)
            current_state = next_state
            
        return np.array(self.trajectory)