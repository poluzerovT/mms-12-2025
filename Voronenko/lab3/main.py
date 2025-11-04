import numpy as np
from typing import List, Tuple, Dict, Callable, Any
import math
from collections import Counter

class PrisonersDilemma:
    def __init__(self):
        self.payoff_matrix = {
            (0, 0): (3, 3),
            (0, 1): (0, 5),
            (1, 0): (5, 0),
            (1, 1): (1, 1)
        }
        self.num_games = 200

    def calculate_scores(self, move_a: int, move_b: int) -> Tuple[int, int]:
        return self.payoff_matrix[(move_a, move_b)]

    def get_dominant_series_length(self, scores_a: List[int], scores_b: List[int]) -> int:
        max_series = 0
        current_series = 0

        for score_a, score_b in zip(scores_a, scores_b):
            if (score_a == 5 and score_b == 0) or (score_a == 0 and score_b == 5):
                current_series += 1
                max_series = max(max_series, current_series)
            else:
                current_series = 0

        return max_series


def strategy_alex(history_a: List[int], history_b: List[int]) -> int:
    return 1


def strategy_bob(history_a: List[int], history_b: List[int]) -> int:
    return 0


def strategy_clara(history_a: List[int], history_b: List[int]) -> int:
    if not history_b:
        return 0
    return history_b[-1]


def strategy_denis(history_a: List[int], history_b: List[int]) -> int:
    if not history_b:
        return 0
    return 1 - history_b[-1]


def strategy_emma(history_a: List[int], history_b: List[int]) -> int:
    game_number = len(history_a) + 1
    if game_number % 20 == 0:
        return 1
    return 0


def strategy_frida(history_a: List[int], history_b: List[int]) -> int:
    if not history_b:
        return 0
    if history_b[-1] == 1:
        return 1
    return 0


def strategy_george(history_a: List[int], history_b: List[int]) -> int:
    if not history_b:
        return 0
    if len(history_b) >= 2 and history_b[-1] == 1 and history_b[-2] == 1:
        return 1
    if history_b[-1] == 1 and len(history_b) % 5 == 0:
        return 0
    return history_b[-1]



def strategy_napk(history_a: List[int], history_b: List[int]) -> int:
    return np.random.randint(0, 2)


def strategy_ivan(history_a: List[int], history_b: List[int]) -> int:
    return 0 if np.random.random() < 0.9 else 1


def strategy_jack(history_a: List[int], history_b: List[int]) -> int:
    if not history_b:
        return 0
    if history_b[-1] == 0:
        return 0
    else:
        return 0 if np.random.random() < 0.25 else 1


def strategy_kevin(history_a: List[int], history_b: List[int]) -> int:
    if not history_b:
        return 0
    if np.random.random() < 0.25:
        return 1 - history_b[-1]
    else:
        return history_b[-1]


def strategy_lucas(history_a: List[int], history_b: List[int]) -> int:
    if not hasattr(strategy_lucas, 'period'):
        strategy_lucas.period = np.random.randint(1, 51)

    game_number = len(history_a) + 1
    return 1 if game_number % strategy_lucas.period == 0 else 0


def strategy_max(history_a: List[int], history_b: List[int]) -> int:
    if not hasattr(strategy_max, 'current_move'):
        strategy_max.current_move = 0
        strategy_max.remaining_moves = np.random.randint(0, 21)

    if strategy_max.remaining_moves == 0:
        strategy_max.current_move = 1 - strategy_max.current_move
        strategy_max.remaining_moves = np.random.randint(0, 21)

    strategy_max.remaining_moves -= 1
    return strategy_max.current_move


def strategy_natan(history_a: List[int], history_b: List[int]) -> int:
    if not history_b:
        return 0

    recent_moves = history_b[-10:] if len(history_b) >= 10 else history_b
    betrayal_rate = sum(recent_moves) / len(recent_moves) if recent_moves else 0

    base_coop_prob = 0.7

    coop_prob = base_coop_prob * (1 - betrayal_rate)

    return 0 if np.random.random() < coop_prob else 1


class Statistics:
    @staticmethod
    def mean(values: List[float]) -> float:
        return sum(values) / len(values) if values else 0

    @staticmethod
    def variance(values: List[float]) -> float:
        if len(values) < 2:
            return 0
        mean_val = Statistics.mean(values)
        return sum((x - mean_val) ** 2 for x in values) / (len(values) - 1)

    @staticmethod
    def median(values: List[float]) -> float:
        if not values:
            return 0
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        if n % 2 == 1:
            return sorted_vals[n // 2]
        else:
            return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2

    @staticmethod
    def mode(values: List[float]) -> float:
        if not values:
            return 0

        k = int(1 + math.log2(len(values))) if len(values) > 1 else 1

        min_val, max_val = min(values), max(values)
        if min_val == max_val:
            return min_val

        bin_width = (max_val - min_val) / k
        bins = [0] * k

        for value in values:
            bin_index = min(int((value - min_val) / bin_width), k - 1)
            bins[bin_index] += 1

        max_freq_index = bins.index(max(bins))

        bin_start = min_val + max_freq_index * bin_width
        bin_end = bin_start + bin_width
        bin_values = [v for v in values if bin_start <= v < bin_end]

        return sum(bin_values) / len(bin_values) if bin_values else (bin_start + bin_end) / 2


class StochasticTournament:
    def __init__(self, num_simulations: int = 1000):
        self.game = PrisonersDilemma()
        self.num_simulations = num_simulations

        self.deterministic_strategies = {
            'Alex': strategy_alex,
            'Bob': strategy_bob,
            'Clara': strategy_clara,
            'Denis': strategy_denis,
            'Emma': strategy_emma,
            'Frida': strategy_frida,
            'George': strategy_george
        }

        self.stochastic_strategies = {
            'Hank': strategy_napk,
            'Ivan': strategy_ivan,
            'Jack': strategy_jack,
            'Kevin': strategy_kevin,
            'Lucas': strategy_lucas,
            'Max': strategy_max,
            'Natan': strategy_natan
        }

        self.all_strategies = {**self.deterministic_strategies, **self.stochastic_strategies}

    def play_multiple_games(self, strategy_a: Callable, strategy_b: Callable) -> Dict[str, float]:
        scores_a_all = []
        scores_b_all = []

        for sim in range(self.num_simulations):
            self._reset_strategies()

            history_a = []
            history_b = []
            total_a = 0
            total_b = 0

            for game_num in range(self.game.num_games):
                move_a = strategy_a(history_a, history_b)
                move_b = strategy_b(history_b, history_a)

                score_a, score_b = self.game.calculate_scores(move_a, move_b)

                history_a.append(move_a)
                history_b.append(move_b)
                total_a += score_a
                total_b += score_b

            scores_a_all.append(total_a)
            scores_b_all.append(total_b)

        return {
            'A_mean': Statistics.mean(scores_a_all),
            'A_median': Statistics.median(scores_a_all),
            'A_mode': Statistics.mode(scores_a_all),
            'A_variance': Statistics.variance(scores_a_all),
            'B_mean': Statistics.mean(scores_b_all),
            'B_median': Statistics.median(scores_b_all),
            'B_mode': Statistics.mode(scores_b_all),
            'B_variance': Statistics.variance(scores_b_all),
        }

    def _reset_strategies(self):
        if hasattr(strategy_lucas, 'period'):
            delattr(strategy_lucas, 'period')
        if hasattr(strategy_max, 'current_move'):
            delattr(strategy_max, 'current_move')
        if hasattr(strategy_max, 'remaining_moves'):
            delattr(strategy_max, 'remaining_moves')

    def run_comparison(self):
        print("СРАВНЕНИЕ ДЕТЕРМИНИРОВАННЫХ И СТОХАСТИЧЕСКИХ СТРАТЕГИЙ")
        print("=" * 100)
        print(f"Количество симуляций на пару: {self.num_simulations}")
        print()

        stochastic_names = list(self.stochastic_strategies.keys())
        deterministic_names = list(self.deterministic_strategies.keys())

        for stoch_name in stochastic_names:
            print(f"\nАнализ стохастической стратегии: {stoch_name}")
            print("-" * 80)

            results = {}
            for det_name in deterministic_names:
                stats = self.play_multiple_games(
                    self.stochastic_strategies[stoch_name],
                    self.deterministic_strategies[det_name]
                )
                results[det_name] = stats

            self._print_comparison_table(stoch_name, results, deterministic_names)

    def _print_comparison_table(self, stoch_name: str, results: Dict, opponents: List[str]):
        print(f"\nСтратегия {stoch_name} против детерминированных стратегий:")
        print("Противник | Среднее | Медиана | Мода   | Дисперсия")
        print("-" * 60)

        for opponent in opponents:
            stats = results[opponent]
            print(f"{opponent:^9} | {stats['A_mean']:^7.1f} | {stats['A_median']:^7.1f} | "
                  f"{stats['A_mode']:^6.1f} | {stats['A_variance']:^9.1f}")

    def run_stochastic_tournament(self):
        print("\n\nТУРНИР СТОХАСТИЧЕСКИХ СТРАТЕГИЙ")
        print("=" * 100)

        stochastic_names = list(self.stochastic_strategies.keys())
        results_summary = {}

        for i, name_a in enumerate(stochastic_names):
            opponent_scores = []
            for name_b in stochastic_names:
                if name_a != name_b:
                    stats = self.play_multiple_games(
                        self.stochastic_strategies[name_a],
                        self.stochastic_strategies[name_b]
                    )
                    opponent_scores.append(stats['A_mean'])

            avg_score = sum(opponent_scores) / len(opponent_scores) if opponent_scores else 0
            results_summary[name_a] = avg_score

        sorted_results = sorted(results_summary.items(), key=lambda x: x[1], reverse=True)

        print("\nРейтинг стохастических стратегий:")
        print("Ранг | Стратегия | Средние очки")
        print("-" * 35)
        for rank, (name, score) in enumerate(sorted_results, 1):
            print(f"{rank:^4} | {name:^9} | {score:^12.1f}")

def main():
    tournament = StochasticTournament(num_simulations=500)
    tournament.run_comparison()
    tournament.run_stochastic_tournament()

if __name__ == "__main__":
    np.random.seed(42)
    main()