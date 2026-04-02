import numpy as np
from .base_model import DiscreteModel

class HostParasiteModel(DiscreteModel):
    """
    Модель 'Хозяин-Паразит' (Николсон, Бейли).
    state[0] -> x (хозяева)
    state[1] -> y (паразиты)
    """
    def step(self, state):
        x_t = state[0]
        y_t = state[1]
        
        b = self.params['b'] # Рождаемость хозяев
        a = self.params['a'] # Эффективность поиска паразитов
        c = self.params['c'] # К-во паразитов из одного хозяина
        
        # Общий член exp(-a * y_t) - доля выживших хозяев
        prob_survival = np.exp(-a * y_t)
        
        # x(t+1) = b * x(t) * exp(-a * y(t))
        x_next = b * x_t * prob_survival
        
        # y(t+1) = c * x(t) * (1 - exp(-a * y(t)))
        y_next = c * x_t * (1 - prob_survival)
        
        return np.array([x_next, y_next])