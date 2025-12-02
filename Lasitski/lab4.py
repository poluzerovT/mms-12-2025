from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Sequence, Tuple

import math

import numpy as np

import matplotlib

matplotlib.use("Agg")  # гарантируем работу без GUI
import matplotlib.pyplot as plt


ScalarMap = Callable[[float], float]


@dataclass(frozen=True)
class HostParasiteParams:
    a: float
    b: float
    c: float


def logistic_rule(r: float) -> ScalarMap:
    return lambda x: r * x * (1.0 - x)


def moran_rule(r: float) -> ScalarMap:
    return lambda x: x * math.exp(r * (1.0 - x))


def iterate_scalar_map(rule: ScalarMap, x0: float, steps: int) -> np.ndarray:
    values = np.empty(steps + 1)
    values[0] = x0
    for i in range(steps):
        values[i + 1] = rule(values[i])
    return values


def iterate_host_parasite(params: HostParasiteParams, x0: float, y0: float, steps: int) -> np.ndarray:
    values = np.empty((steps + 1, 2))
    values[0, 0] = x0
    values[0, 1] = y0
    for i in range(steps):
        x_t, y_t = values[i]
        survival = math.exp(-params.a * y_t)
        x_next = params.b * x_t * survival
        y_next = params.c * x_t * (1.0 - survival)
        values[i + 1, 0] = x_next
        values[i + 1, 1] = y_next
    return values


def _regime_from_tail(tail: np.ndarray, tolerance: float = 1e-3, max_cycle: int = 16) -> str:
    if tail.size == 0:
        return "недостаточно данных"
    if not np.all(np.isfinite(tail)):
        return "расходимость"
    if np.max(np.abs(tail)) > 1e6:
        return "расходимость"
    diffs = np.diff(tail)
    if diffs.size == 0 or (np.max(diffs) < tolerance and np.min(diffs) > -tolerance):
        return "устойчивое равновесие"

    unique: List[float] = []
    for value in tail[-100:]:
        if not any(abs(value - u) < tolerance for u in unique):
            unique.append(value)
        if len(unique) > max_cycle:
            return "хаотическое поведение"
    return f"{len(unique)}-цикл"


def explore_logistic(r_values: Sequence[float], x0_values: Sequence[float], steps: int = 1500, burn_in: int = 500):
    records = []
    for r in r_values:
        rule = logistic_rule(r)
        for x0 in x0_values:
            seq = iterate_scalar_map(rule, x0, steps)
            tail = seq[burn_in:]
            regime = _regime_from_tail(tail)
            records.append(
                {
                    "model": "logistic",
                    "r": r,
                    "x0": x0,
                    "regime": regime,
                    "tail_mean": float(np.mean(tail[-100:])),
                    "tail_std": float(np.std(tail[-100:])),
                }
            )
    return records


def explore_moran(r_values: Sequence[float], x0_values: Sequence[float], steps: int = 600, burn_in: int = 200):
    records = []
    for r in r_values:
        rule = moran_rule(r)
        for x0 in x0_values:
            seq = iterate_scalar_map(rule, x0, steps)
            tail = seq[burn_in:]
            regime = _regime_from_tail(tail, tolerance=5e-3)
            records.append(
                {
                    "model": "moran",
                    "r": r,
                    "x0": x0,
                    "regime": regime,
                    "tail_mean": float(np.mean(tail[-100:])),
                    "tail_std": float(np.std(tail[-100:])),
                }
            )
    return records


def explore_host_parasite(
    params_list: Sequence[HostParasiteParams],
    initials: Sequence[Tuple[float, float]],
    steps: int = 200,
    burn_in: int = 50,
):
    records = []
    for params in params_list:
        for x0, y0 in initials:
            seq = iterate_host_parasite(params, x0, y0, steps)
            tail = seq[burn_in:]
            host_tail = tail[:, 0]
            parasite_tail = tail[:, 1]
            host_span = float(np.max(host_tail) - np.min(host_tail))
            parasite_span = float(np.max(parasite_tail) - np.min(parasite_tail))
            diverging = (not np.all(np.isfinite(seq))) or float(np.max(np.abs(seq))) > 1e6
            if diverging:
                regime = "неограниченный рост"
                host_mean = float("inf") if np.max(host_tail) > 1e6 else float(np.mean(host_tail[-50:]))
                parasite_mean = float("inf") if np.max(parasite_tail) > 1e6 else float(np.mean(parasite_tail[-50:]))
            elif host_span < 1e-3 and parasite_span < 1e-3:
                regime = "равновесие"
                host_mean = float(np.mean(host_tail[-50:]))
                parasite_mean = float(np.mean(parasite_tail[-50:]))
            else:
                regime = "устойчивые колебания"
                host_mean = float(np.mean(host_tail[-50:]))
                parasite_mean = float(np.mean(parasite_tail[-50:]))
            records.append(
                {
                    "model": "host-parasite",
                    "params": params,
                    "x0": x0,
                    "y0": y0,
                    "regime": regime,
                    "host_mean": host_mean,
                    "parasite_mean": parasite_mean,
                }
            )
    return records


def _group_by_parameter(records: List[Dict], key: str) -> Dict[float, List[Dict]]:
    grouped: Dict[float, List[Dict]] = {}
    for record in records:
        grouped.setdefault(record[key], []).append(record)
    return grouped


def print_scalar_summary(records: List[Dict], title: str) -> None:
    print(f"\n{title}")
    grouped = _group_by_parameter(records, "r")
    for r_value, group in grouped.items():
        regimes = {entry["regime"] for entry in group}
        means = np.mean([entry["tail_mean"] for entry in group])
        stds = np.mean([entry["tail_std"] for entry in group])
        print(f"  r = {r_value:.3f}: режимы {', '.join(regimes)} | ⟨x⟩ ≈ {means:.3f}, σ ≈ {stds:.3f}")


def print_host_parasite_summary(records: List[Dict]) -> None:
    print("\nМодель хозяин–паразит (Николсон–Бейли)")
    for record in records:
        p = record["params"]
        print(
            "  "
            f"a={p.a:.2f}, b={p.b:.2f}, c={p.c:.2f}, x0={record['x0']:.2f}, y0={record['y0']:.2f} -> "
            f"{record['regime']} (⟨x⟩≈{record['host_mean']:.3f}, ⟨y⟩≈{record['parasite_mean']:.3f})"
        )


def find_logistic_bifurcations(
    r_start: float = 2.5,
    r_end: float = 4.0,
    samples: int = 150,
    x0: float = 0.2,
    steps: int = 2000,
    burn_in: int = 800,
) -> List[Tuple[float, str, str]]:
    r_values = np.linspace(r_start, r_end, samples)
    last_regime = None
    transitions: List[Tuple[float, str, str]] = []
    for r in r_values:
        regime = _regime_from_tail(
            iterate_scalar_map(logistic_rule(r), x0, steps)[burn_in:], tolerance=5e-4
        )
        if last_regime is not None and regime != last_regime:
            if not transitions or r - transitions[-1][0] > 0.01:
                transitions.append((float(r), last_regime, regime))
        last_regime = regime
    return transitions


def plot_population_examples(output_path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Схожие траектории: логистическая модель с r=2.5, разные x0
    ax = axes[0, 0]
    r_similar = 2.5
    for x0 in (0.1, 0.9):
        seq = iterate_scalar_map(logistic_rule(r_similar), x0, 60)
        ax.plot(seq, label=f"x0={x0}")
    ax.set_title("Логистическая: схожая динамика (r=2.5)")
    ax.set_xlabel("t")
    ax.set_ylabel("x_t")
    ax.legend()

    # Существенно разное поведение: логистическая с r=3.5 и 3.9
    ax = axes[0, 1]
    for r in (3.5, 3.9):
        seq = iterate_scalar_map(logistic_rule(r), 0.2, 160)
        ax.plot(seq, label=f"r={r}")
    ax.set_title("Логистическая: различная динамика")
    ax.set_xlabel("t")
    ax.set_ylabel("x_t")
    ax.legend()

    # Модель Морана: сравнение режимов
    ax = axes[1, 0]
    for r in (0.8, 2.0):
        seq = iterate_scalar_map(moran_rule(r), 0.3, 80)
        ax.plot(seq, label=f"r={r}")
    ax.set_title("Модель Морана")
    ax.set_xlabel("t")
    ax.set_ylabel("x_t")
    ax.legend()

    # Хозяин–паразит: отображаем обе популяции
    ax = axes[1, 1]
    params = HostParasiteParams(a=0.5, b=2.5, c=1.1)
    seq = iterate_host_parasite(params, x0=0.8, y0=0.2, steps=80)
    ax.plot(seq[:, 0], label="x_t (хозяева)")
    ax.plot(seq[:, 1], label="y_t (паразиты)")
    ax.set_title("Николсон–Бейли: колебания")
    ax.set_xlabel("t")
    ax.set_ylabel("численность")
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main() -> None:
    logistic_rs = np.linspace(2.5, 3.8, 6)
    logistic_x0 = [0.05, 0.2, 0.6, 0.9]
    logistic_records = explore_logistic(logistic_rs, logistic_x0)
    print_scalar_summary(logistic_records, "Логистическая модель")

    moran_rs = [0.5, 1.0, 1.5, 2.5]
    moran_x0 = [0.1, 0.4, 0.9]
    moran_records = explore_moran(moran_rs, moran_x0)
    print_scalar_summary(moran_records, "Модель Морана")

    params_list = [
        HostParasiteParams(a=0.3, b=1.8, c=0.9),
        HostParasiteParams(a=0.5, b=2.5, c=1.1),
        HostParasiteParams(a=0.7, b=3.0, c=1.2),
    ]
    initials = [(0.5, 0.2), (0.9, 0.4)]
    host_records = explore_host_parasite(params_list, initials)
    print_host_parasite_summary(host_records)

    bifurcations = find_logistic_bifurcations()
    print("\nПороговые значения r (логистическая модель):")
    for r, src, dst in bifurcations:
        print(f"  r ≈ {r:.3f}: {src} → {dst}")

    plot_path = Path(__file__).with_name("lab4_trajectории.png")
    plot_population_examples(plot_path)
    print(f"\nГрафики сохранены в {plot_path.resolve()}")


if __name__ == "__main__":
    main()

