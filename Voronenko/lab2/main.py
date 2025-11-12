import numpy as np
from typing import List, Tuple, Dict, Callable

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


class StrategyTournament:
    def __init__(self):
        self.game = PrisonersDilemma()
        self.strategies = {
            'Alex': strategy_alex,
            'Bob': strategy_bob,
            'Clara': strategy_clara,
            'Denis': strategy_denis,
            'Emma': strategy_emma,
            'Frida': strategy_frida,
            'George': strategy_george
        }

    def play_single_game(self, strategy_a: Callable, strategy_b: Callable) -> Dict:
        history_a = []
        history_b = []
        scores_a = []
        scores_b = []

        for game_num in range(self.game.num_games):
            move_a = strategy_a(history_a, history_b)
            move_b = strategy_b(history_b, history_a)

            score_a, score_b = self.game.calculate_scores(move_a, move_b)

            history_a.append(move_a)
            history_b.append(move_b)
            scores_a.append(score_a)
            scores_b.append(score_b)

        total_a = sum(scores_a)
        total_b = sum(scores_b)
        dominant_series = self.game.get_dominant_series_length(scores_a, scores_b)

        return {
            'total_a': total_a,
            'total_b': total_b,
            'dominant_series': dominant_series,
            'scores_a': scores_a,
            'scores_b': scores_b
        }

    def run_tournament(self):
        results = {}
        strategy_names = list(self.strategies.keys())

        print("ТУРНИР СТРАТЕГИЙ В ДИЛЕММЕ ЗАКЛЮЧЕННЫХ")
        print("=" * 80)

        for i, name_a in enumerate(strategy_names):
            for j, name_b in enumerate(strategy_names):
                result = self.play_single_game(
                    self.strategies[name_a],
                    self.strategies[name_b]
                )
                results[(name_a, name_b)] = result

        self.analyze_results(results, strategy_names)

    def analyze_results(self, results: Dict, strategy_names: List[str]):
        print("\n1. ОБЩИЕ ОЧКИ (сумма за 200 игр)")
        print("Строка = нападающий, Столбец = защитник")
        print("-" * 80)
        header = "Стратегия | " + " | ".join(f"{name:^8}" for name in strategy_names)
        print(header)
        print("-" * len(header))

        for name_a in strategy_names:
            row = f"{name_a:^9} | "
            for name_b in strategy_names:
                score = results[(name_a, name_b)]['total_a']
                row += f"{score:^8} | "
            print(row)

        print("\n\n2. ДЛИНА НАИБОЛЬШЕЙ ДОМИНИРУЮЩЕЙ СЕРИИ")
        print("(доминирование игрока строки над игроком столбца)")
        print("-" * 80)
        header = "Стратегия | " + " | ".join(f"{name:^8}" for name in strategy_names)
        print(header)
        print("-" * len(header))

        for name_a in strategy_names:
            row = f"{name_a:^9} | "
            for name_b in strategy_names:
                series = results[(name_a, name_b)]['dominant_series']
                row += f"{series:^8} | "
            print(row)

        print("\n\n3. СВОДНАЯ СТАТИСТИКА ПО СТРАТЕГИЯМ")
        print("-" * 80)
        summary = []

        for name in strategy_names:
            total_score = 0
            total_games = 0

            for opponent in strategy_names:
                total_score += results[(name, opponent)]['total_a']
                total_games += 1

            avg_score = total_score / total_games
            summary.append((name, avg_score))

        summary.sort(key=lambda x: x[1], reverse=True)

        print("Ранг | Стратегия | Средние очки")
        print("-" * 35)
        for rank, (name, avg_score) in enumerate(summary, 1):
            print(f"{rank:^4} | {name:^9} | {avg_score:^12.1f}")

def main():
    tournament = StrategyTournament()
    tournament.run_tournament()

if __name__ == "__main__":
    main()