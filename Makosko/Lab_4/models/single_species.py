import numpy as np
from .base_model import DiscreteModel


class ExponentialModel(DiscreteModel):
    """
    Экспоненциальный рост:
    x(t+1) = r * x(t)
    """
    def step(self, x):
        r = self.params['r']
        return r * x
    
class LogisticModel(DiscreteModel):
    """
    Логистическая модель:
    x(t+1) = r * x(t) * (1 - x(t))
    """
    def step(self, x):
        r = self.params['r']
        next_val = r * x * (1 - x)
        return next_val

class MoranModel(DiscreteModel):
    """
    Модель Морана (Рикера):
    x(t+1) = x(t) * exp(r * (1 - x(t)))
    """
    def step(self, x):
        r = self.params['r']
        return x * np.exp(r * (1 - x))

