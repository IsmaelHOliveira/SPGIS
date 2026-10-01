"""
Framework de Benchmarking e Comparação de Algoritmos de Ordenação.
Gera tabelas estatísticas em Markdown, CSV e gráficos comparativos PNG.
"""

import argparse
from collections import defaultdict
from html import escape
import os
import random
import time
from typing import Callable, Dict, List, Tuple

from student_template import my_authorial_sort
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
        print(f"\nExecutando benchmarks para distribuição: [{dist.upper()}]")
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


def print_moves_summary(results: dict, sizes: List[int]):
    """Imprime uma tabela Markdown com as movimentações médias."""
    for dist, algs in results.items():
        print(f"\n### Resultados: Distribuição `{dist}` (Movimentações)")
        header = "| Algoritmo | " + " | ".join(f"N={s}" for s in sizes) + " |"
        sep = "| :--- | " + " | ".join(":---:" for _ in sizes) + " |"
        print(header)
        print(sep)
        for alg_name, size_data in algs.items():
            row = [alg_name]
            for s in sizes:
                row.append(f"{size_data[s]['moves']:.1f}" if s in size_data else "—")
            print("| " + " | ".join(row) + " |")


def _svg_line_chart(
    x: int,
    y: int,
    width: int,
    height: int,
    title: str,
    metric: str,
    y_label: str,
    algs: dict,
    sizes: List[int],
    colors: List[str],
) -> str:
    """Desenha um gráfico de linhas SVG sem bibliotecas externas."""
    left, top, right, bottom = 62, 30, 16, 108
    plot_width = width - left - right
    plot_height = height - top - bottom
    values = [data[metric] for data in algs.values() for data in data.values()]
    y_max = max(values, default=1.0)
    y_max = max(1.0, y_max * 1.1)

    def px(index: int) -> float:
        return x + left + (plot_width * index / max(1, len(sizes) - 1))

    def py(value: float) -> float:
        return y + top + plot_height - (value / y_max * plot_height)

    parts = [
        f'<g>',
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="#ffffff" stroke="#cbd5e1"/>',
        f'<text x="{x + width / 2}" y="{y + 18}" text-anchor="middle" font-size="14" font-weight="bold">{escape(title)}</text>',
    ]

    for tick in range(6):
        value = y_max * tick / 5
        tick_y = py(value)
        parts.append(f'<line x1="{x + left}" y1="{tick_y:.2f}" x2="{x + width - right}" y2="{tick_y:.2f}" stroke="#e2e8f0"/>')
        parts.append(f'<text x="{x + left - 6}" y="{tick_y + 4:.2f}" text-anchor="end" font-size="10">{value:.0f}</text>')

    parts.append(f'<line x1="{x + left}" y1="{y + top}" x2="{x + left}" y2="{y + top + plot_height}" stroke="#334155"/>')
    parts.append(f'<line x1="{x + left}" y1="{y + top + plot_height}" x2="{x + width - right}" y2="{y + top + plot_height}" stroke="#334155"/>')
    parts.append(f'<text x="{x + 14}" y="{y + top + plot_height / 2}" transform="rotate(-90 {x + 14} {y + top + plot_height / 2})" text-anchor="middle" font-size="11">{escape(y_label)}</text>')

    for index, size in enumerate(sizes):
        parts.append(f'<text x="{px(index):.2f}" y="{y + top + plot_height + 17}" text-anchor="middle" font-size="10">{size}</text>')
    parts.append(f'<text x="{x + left + plot_width / 2}" y="{y + top + plot_height + 35}" text-anchor="middle" font-size="11">Tamanho da entrada (N)</text>')

    for color_index, (name, size_data) in enumerate(algs.items()):
        color = colors[color_index % len(colors)]
        points = [(px(index), py(size_data[size][metric])) for index, size in enumerate(sizes) if size in size_data]
        if not points:
            continue
        point_text = " ".join(f"{point_x:.2f},{point_y:.2f}" for point_x, point_y in points)
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{point_text}"/>')
        for point_x, point_y in points:
            parts.append(f'<circle cx="{point_x:.2f}" cy="{point_y:.2f}" r="3" fill="{color}"/>')
        legend_x = x + 12 + (color_index % 2) * (width / 2)
        legend_y = y + height - 48 + (color_index // 2) * 15
        parts.append(f'<line x1="{legend_x}" y1="{legend_y}" x2="{legend_x + 14}" y2="{legend_y}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="{legend_x + 19}" y="{legend_y + 4}" font-size="10">{escape(name)}</text>')

    parts.append('</g>')
    return "".join(parts)


def write_svg_benchmark_results(results: dict, output_path: str = "benchmark_results.svg"):
    """Gera um gráfico SVG de tempo, comparações e movimentações sem matplotlib."""
    base_path, extension = os.path.splitext(output_path)
    if extension.lower() != ".svg":
        output_path = f"{base_path}.svg"

    chart_width, chart_height, row_height = 470, 310, 350
    distributions = list(results.keys())
    total_width = chart_width * 3
    total_height = 50 + row_height * len(distributions)
    # Paleta padrão do Matplotlib, preservando as cores do gráfico original.
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<text x="{total_width / 2}" y="28" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" font-weight="bold">Benchmark de Algoritmos de Ordenação</text>',
    ]

    for row_index, distribution in enumerate(distributions):
        row_y = 50 + row_index * row_height
        algs = results[distribution]
        sizes = sorted({size for size_data in algs.values() for size in size_data})
        parts.append(f'<text x="12" y="{row_y + 14}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Distribuição: {escape(distribution)}</text>')
        parts.append(_svg_line_chart(0, row_y + 20, chart_width, chart_height - 20, "Tempo médio", "time_ms", "Tempo (ms)", algs, sizes, colors))
        parts.append(_svg_line_chart(chart_width, row_y + 20, chart_width, chart_height - 20, "Comparações", "comps", "Comparações", algs, sizes, colors))
        parts.append(_svg_line_chart(chart_width * 2, row_y + 20, chart_width, chart_height - 20, "Movimentações", "moves", "Movimentações", algs, sizes, colors))

    parts.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as svg_file:
        svg_file.write("\n".join(parts))
    print(f"\nGráfico SVG salvo com sucesso em: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Benchmark de Algoritmos de Ordenação — APA")
    parser.add_argument("--trials", type=int, default=3, help="Número de repetições por teste")
    parser.add_argument("--plot", type=str, default="benchmark_results.svg", help="Caminho para salvar o gráfico SVG")
    args = parser.parse_args()

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Meu Algoritimo (SPGIS)": my_authorial_sort,
    }

    sizes = [10, 50, 100, 250, 500, 1000]
    distributions = ["random", "sorted", "reverse", "duplicates", "almost_sorted"]

    random.seed(42)
    results = run_benchmark(algorithms, sizes, distributions, trials=args.trials)
    print_markdown_summary(results, sizes)
    print_moves_summary(results, sizes)
    write_svg_benchmark_results(results, args.plot)


if __name__ == "__main__":
    main()
