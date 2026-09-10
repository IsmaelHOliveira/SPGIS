"""
Framework de Benchmarking e Comparação de Algoritmos de Ordenação.
Gera tabelas estatísticas em Markdown, CSV e gráficos comparativos PNG.
"""

import argparse
from collections import defaultdict
import os
import random
import time
from typing import Callable, Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from authorial import dpes_sort
from classical import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)


def generate_dataset(n: int, distribution: str) -> List[int]:
    """Gera vetores para testes com diferentes distribuições de dados."""
    if distribution == "random":
        return [random.randint(0, 10 * n) for _ in range(n)]
    elif distribution == "sorted":
        return list(range(n))
    elif distribution == "reverse":
        return list(range(n, 0, -1))
    elif distribution == "duplicates":
        return [random.choice([1, 2, 3, 5, 8]) for _ in range(n)]
    elif distribution == "almost_sorted":
        arr = list(range(n))
        swaps = max(1, n // 20)  # ~5% de trocas aleatórias
        for _ in range(swaps):
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    else:
        raise ValueError(f"Distribuição desconhecida: {distribution}")


def run_benchmark(
    algorithms: Dict[str, Callable[[List], Tuple[List, int, int]]],
    sizes: List[int],
    distributions: List[str],
    trials: int = 3,
) -> Dict[str, Dict[str, Dict[int, Dict[str, float]]]]:
    """
    Executa medições de tempo, comparações e movimentações para cada algoritmo,
    tamanho e distribuição.
    """
    # results[dist][alg_name][size] = {'time_ms': ..., 'comps': ..., 'moves': ...}
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    for dist in distributions:
        print(f"\n📊 Executando benchmarks para distribuição: [{dist.upper()}]")
        for size in sizes:
            print(f"  -> Tamanho N = {size}...")
            # Gera datasets fixos por repetição para garantir comparação justa
            datasets = [generate_dataset(size, dist) for _ in range(trials)]

            for name, fn in algorithms.items():
                # Para Bubble/Selection/Insertion, evita tamanhos excessivos que demoram muito
                if size > 1500 and name in ("Bubble Sort", "Selection Sort", "Insertion Sort") and dist in ("random", "reverse"):
                    continue

                times = []
                comps = []
                moves = []

                for data in datasets:
                    data_copy = list(data)
                    start = time.perf_counter()
                    res, c, m = fn(data_copy)
                    elapsed_ms = (time.perf_counter() - start) * 1000.0

                    # Validação de sanidade
                    assert res == sorted(data), f"Erro de ordenação em {name}!"

                    times.append(elapsed_ms)
                    comps.append(c)
                    moves.append(m)

                results[dist][name][size] = {
                    "time_ms": sum(times) / len(times),
                    "comps": sum(comps) / len(comps),
                    "moves": sum(moves) / len(moves),
                }

    return results


def print_markdown_summary(results: dict, sizes: List[int]):
    """Imprime tabela formatada em Markdown com os resultados comparativos."""
    for dist, algs in results.items():
        print(f"\n### Resultados: Distribuição `{dist}` (Tempo em ms)")
        header = "| Algoritmo | " + " | ".join(f"N={s}" for s in sizes) + " |"
        sep = "| :--- | " + " | ".join(":---:" for _ in sizes) + " |"
        print(header)
        print(sep)
        for alg_name, size_data in algs.items():
            row = [alg_name]
            for s in sizes:
                if s in size_data:
                    row.append(f"{size_data[s]['time_ms']:.3f} ms")
                else:
                    row.append("—")
            print("| " + " | ".join(row) + " |")


def plot_benchmark_results(results: dict, output_path: str = "benchmark_results.png"):
    """Gera gráficos de curvas de tempo e comparações usando matplotlib."""
    distributions = list(results.keys())
    fig, axes = plt.subplots(len(distributions), 2, figsize=(14, 4 * len(distributions)))

    if len(distributions) == 1:
        axes = [axes]

    for idx, dist in enumerate(distributions):
        ax_time = axes[idx][0]
        ax_comps = axes[idx][1]

        for alg_name, size_map in results[dist].items():
            sizes = sorted(size_map.keys())
            times = [size_map[s]["time_ms"] for s in sizes]
            comps = [size_map[s]["comps"] for s in sizes]

            ax_time.plot(sizes, times, marker="o", label=alg_name)
            ax_comps.plot(sizes, comps, marker="s", label=alg_name)

        ax_time.set_title(f"Tempo de Execução (ms) — [{dist.title()}]")
        ax_time.set_xlabel("Tamanho da Entrada (N)")
        ax_time.set_ylabel("Tempo Médio (ms)")
        ax_time.grid(True, linestyle="--", alpha=0.6)
        ax_time.legend()

        ax_comps.set_title(f"Número de Comparações — [{dist.title()}]")
        ax_comps.set_xlabel("Tamanho da Entrada (N)")
        ax_comps.set_ylabel("Comparações")
        ax_comps.grid(True, linestyle="--", alpha=0.6)
        ax_comps.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"\n🖼️ Gráfico salvo com sucesso em: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Benchmark de Algoritmos de Ordenação — APA")
    parser.add_argument("--trials", type=int, default=3, help="Número de repetições por teste")
    parser.add_argument("--plot", type=str, default="benchmark_results.png", help="Caminho para salvar o gráfico")
    args = parser.parse_args()

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Authorial (DPES)": dpes_sort,
    }

    sizes = [10, 50, 100, 250, 500, 1000]
    distributions = ["random", "sorted", "reverse", "duplicates", "almost_sorted"]

    random.seed(42)
    results = run_benchmark(algorithms, sizes, distributions, trials=args.trials)
    print_markdown_summary(results, sizes)
    plot_benchmark_results(results, args.plot)


if __name__ == "__main__":
    main()
