import random
import math
from typing import Any

W = [[3, 0], [5, 1]]

def alex(my_history, opponent_history, round_index):
    return 1

def bob(my_history, opponent_history, round_index):
    return 0

def clara(my_history, opponent_history, round_index):
    if round_index == 1:
        return 0
    return opponent_history[-1]

def denis(my_history, opponent_history, round_index):
    if round_index == 1:
        return 0
    return 1 - opponent_history[-1]

def emma(my_history, opponent_history, round_index):
    if round_index % 20 == 0:
        return 1
    return 0

def frida(my_history, opponent_history, round_index):
    if 1 in opponent_history:
        return 1
    return 0

def george(my_history, opponent_history, round_index):
    if round_index == 1:
        return 0
    my_last = my_history[-1]
    opp_last = opponent_history[-1]
    last_payoff = W[my_last][opp_last]
    if last_payoff in (1, 3, 5):
        return my_last
    return 1 - my_last

def hank(my_history, opponent_history, round_index):
    return random.randint(0, 1)

def ivan(my_history, opponent_history, round_index):
    return 0 if random.random() < 0.9 else 1

def jack(my_history, opponent_history, round_index):
    if round_index == 1:
        return 0
    if opponent_history[-1] == 0:
        return 0
    return 0 if random.random() < 0.25 else 1

def kevin(my_history, opponent_history, round_index):
    if round_index == 1:
        return 0
    base = opponent_history[-1]
    if random.random() < 0.25:
        return 1 - base
    return base

class LucasStrategy:
    def __init__(self):
        self.k = random.randint(1, 50)
    def __call__(self, my_history, opponent_history, round_index):
        if round_index % self.k == 0:
            return 1
        return 0

class MaxStrategy:
    def __init__(self):
        self.current = 0
        self.remaining = random.randint(0, 20)
    def __call__(self, my_history, opponent_history, round_index):
        if self.remaining <= 0:
            self.current = 1 - self.current
            self.remaining = random.randint(0, 20)
        self.remaining -= 1
        return self.current

class NatanStrategy:
    def __call__(self, my_history, opponent_history, round_index):
        if round_index == 1:
            return 0
        if random.random() < 0.1:
            return random.randint(0, 1)
        my_last = my_history[-1]
        opp_last = opponent_history[-1]
        last_payoff = W[my_last][opp_last]
        if last_payoff in (3, 5):
            return my_last
        return my_last if random.random() >= 0.7 else 1 - my_last

def play_match(strategy_a, strategy_b, rounds=200):
    history_a = []
    history_b = []
    score_a = 0
    score_b = 0
    current_dom_a = 0
    current_dom_b = 0
    max_dom_a = 0
    max_dom_b = 0
    for r in range(1, rounds + 1):
        move_a = strategy_a(history_a, history_b, r)
        move_b = strategy_b(history_b, history_a, r)
        history_a.append(move_a)
        history_b.append(move_b)
        s_a = W[move_a][move_b]
        s_b = W[move_b][move_a]
        score_a += s_a
        score_b += s_b
        if move_a == 1 and move_b == 0:
            current_dom_a += 1
            current_dom_b = 0
        elif move_a == 0 and move_b == 1:
            current_dom_b += 1
            current_dom_a = 0
        else:
            current_dom_a = 0
            current_dom_b = 0
        if current_dom_a > max_dom_a:
            max_dom_a = current_dom_a
        if current_dom_b > max_dom_b:
            max_dom_b = current_dom_b
    return score_a, score_b, max_dom_a, max_dom_b

def mean(values):
    if not values:
        return 0.0
    return sum(values) / len(values)

def variance(values):
    n = len(values)
    if n <= 1:
        return 0.0
    m = mean(values)
    return sum((x - m) * (x - m) for x in values) / (n - 1)

def median(values):
    n = len(values)
    if n == 0:
        return 0.0
    s = sorted(values)
    mid = n // 2
    if n % 2 == 1:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2.0

def mode_estimate(values):
    n = len(values)
    if n == 0:
        return 0.0
    min_v = min(values)
    max_v = max(values)
    if min_v == max_v:
        return float(min_v)
    k = int(math.log2(1 + n))
    if k < 1:
        k = 1
    width = (max_v - min_v) / k if k > 0 else 1.0
    if width == 0:
        return float(min_v)
    counts = [0] * k
    bins = [[] for _ in range(k)]
    for x in values:
        idx = int((x - min_v) / width)
        if idx >= k:
            idx = k - 1
        counts[idx] += 1
        bins[idx].append(x)
    best_idx = 0
    best_count = counts[0]
    for i in range(1, k):
        if counts[i] > best_count:
            best_count = counts[i]
            best_idx = i
    if not bins[best_idx]:
        return float(min_v)
    return mean(bins[best_idx])

def deterministic_strategies():
    return {
        "Alex": lambda: alex,
        "Bob": lambda: bob,
        "Clara": lambda: clara,
        "Denis": lambda: denis,
        "Emma": lambda: emma,
        "Frida": lambda: frida,
        "George": lambda: george,
    }

def stochastic_strategies():
    return {
        "Hank": lambda: hank,
        "Ivan": lambda: ivan,
        "Jack": lambda: jack,
        "Kevin": lambda: kevin,
        "Lucas": lambda: LucasStrategy(),
        "Max": lambda: MaxStrategy(),
        "Natan": lambda: NatanStrategy(),
    }

def run_pair(factory_a, factory_b, rounds, simulations):
    scores_a = []
    scores_b = []
    for _ in range(simulations):
        sa, sb, _, _ = play_match(factory_a(), factory_b(), rounds)
        scores_a.append(sa)
        scores_b.append(sb)
    return scores_a, scores_b

def run_all(rounds=200, simulations_for_stochastic=10000):
    det = deterministic_strategies()
    sto = stochastic_strategies()
    all_factories = {**det, **sto}
    names = list(all_factories.keys())
    sto_names = set(sto.keys())
    results = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = names[i]
            b = names[j]
            sims = simulations_for_stochastic if (a in sto_names or b in sto_names) else 1
            sa_list, sb_list = run_pair(all_factories[a], all_factories[b], rounds, sims)
            results.append((a, b, sims, sa_list, sb_list))
    return names, results

def build_matrices(names, results):
    n = len(names)
    idx = {name: i for i, name in enumerate(names)}
    mean_m = [[0.0 for _ in range(n)] for _ in range(n)]
    median_m = [[0.0 for _ in range(n)] for _ in range(n)]
    mode_m = [[0.0 for _ in range(n)] for _ in range(n)]
    var_m = [[0.0 for _ in range(n)] for _ in range(n)]
    for a, b, _, sa, sb in results:
        ia = idx[a]
        ib = idx[b]
        mean_m[ia][ib] = mean(sa)
        mean_m[ib][ia] = mean(sb)
        median_m[ia][ib] = median(sa)
        median_m[ib][ia] = median(sb)
        mode_m[ia][ib] = mode_estimate(sa)
        mode_m[ib][ia] = mode_estimate(sb)
        var_m[ia][ib] = variance(sa)
        var_m[ib][ia] = variance(sb)
    return mean_m, median_m, mode_m, var_m

def write_markdown(results, target_path, names=None, matrices=None):
    with open(target_path, "w", encoding="utf-8") as f:
        f.write("# Лабораторная работа №3. Стохастические стратегии\n\n")
        if names is not None and matrices is not None:
            mean_m, median_m, mode_m, var_m = matrices
            def write_matrix(title, m):
                f.write(f"## {title}\n\n")
                header = "|" + "|".join([""] + names) + "|\n"
                sep = "|" + "|".join([":-"] + [":-:" for _ in names]) + "|\n"
                f.write(header)
                f.write(sep)
                for i, name in enumerate[Any](names):
                    row = [name] + [f"{m[i][j]:.2f}" for j in range(len(names))]
                    f.write("|" + "|".join(row) + "|\n")
                f.write("\n")
            write_matrix("Матрица средних очков", mean_m)
            write_matrix("Матрица медиан очков", median_m)
            write_matrix("Матрица мод", mode_m)
            write_matrix("Матрица дисперсий очков", var_m)
        else:
            f.write("| A | B | n | mean_A | median_A | mode_A | var_A | mean_B | median_B | mode_B | var_B |\n")
            f.write("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
            for a, b, n, sa, sb in results:
                mA = mean(sa)
                mdA = median(sa)
                moA = mode_estimate(sa)
                vA = variance(sa)
                mB = mean(sb)
                mdB = median(sb)
                moB = mode_estimate(sb)
                vB = variance(sb)
                f.write(f"| {a} | {b} | {n} | {mA:.2f} | {mdA:.2f} | {moA:.2f} | {vA:.2f} | {mB:.2f} | {mdB:.2f} | {moB:.2f} | {vB:.2f} |\n")

def print_summary(results):
    print("Итоги парных сравнений (среднее и дисперсия):")
    for a, b, n, sa, sb in results:
        print(f"{a} vs {b} n={n} meanA={mean(sa):.2f} varA={variance(sa):.2f} meanB={mean(sb):.2f} varB={variance(sb):.2f}")

if __name__ == "__main__":
    names, results = run_all()
    print_summary(results)
    mean_m, median_m, mode_m, var_m = build_matrices(names, results)
    print("Матрица средних:")
    for i in range(len(names)):
        print(" ".join(f"{mean_m[i][j]:6.2f}" for j in range(len(names))))
    print("Матрица медиан:")
    for i in range(len(names)):
        print(" ".join(f"{median_m[i][j]:6.2f}" for j in range(len(names))))
    print("Матрица мод:")
    for i in range(len(names)):
        print(" ".join(f"{mode_m[i][j]:6.2f}" for j in range(len(names))))
    print("Матрица дисперсий:")
    for i in range(len(names)):
        print(" ".join(f"{var_m[i][j]:6.2f}" for j in range(len(names))))
    write_markdown(results, "/Users/mihailkoruzn/Documents/fpmi/mms/mms-12-2025/lab3_results.md", names, (mean_m, median_m, mode_m, var_m))