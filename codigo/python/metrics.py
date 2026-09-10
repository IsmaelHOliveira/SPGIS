"""
Módulo de Métricas e Instrumentação de Algoritmos de Ordenação.
Contabiliza comparações, trocas/movimentações de elementos e tempo de execução.
"""

from dataclasses import dataclass
import time
from typing import Any, Callable, List, Tuple


@dataclass
class SortMetrics:
    """Métricas coletadas durante a execução de um algoritmo de ordenação."""
    algorithm_name: str
    input_size: int
    distribution: str
    elapsed_time_sec: float
    comparisons: int
    swaps_or_moves: int
    is_sorted: bool


class InstrumentedList:
    """
    Wrapper transparente sobre lista para rastrear comparações e atribuições/trocas.
    """
    def __init__(self, data: List[Any]):
        self._data = list(data)
        self.comparisons = 0
        self.moves = 0

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int) -> Any:
        return self._data[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self.moves += 1
        self._data[index] = value

    def compare(self, i: int, j: int) -> int:
        """
        Compara elementos nos índices i e j:
        Retorna -1 se data[i] < data[j], 0 se data[i] == data[j], 1 se data[i] > data[j].
        """
        self.comparisons += 1
        if self._data[i] < self._data[j]:
            return -1
        elif self._data[i] > self._data[j]:
            return 1
        return 0

    def compare_val(self, val: Any, j: int) -> int:
        """Compara um valor avulso contra o elemento no índice j."""
        self.comparisons += 1
        if val < self._data[j]:
            return -1
        elif val > self._data[j]:
            return 1
        return 0

    def swap(self, i: int, j: int) -> None:
        """Realiza a troca entre dois índices contabilizando 2 movimentações."""
        if i != j:
            self.moves += 2
            self._data[i], self._data[j] = self._data[j], self._data[i]

    def to_list(self) -> List[Any]:
        return list(self._data)


def measure_sort(
    sort_fn: Callable[[List[Any]], Tuple[List[Any], int, int]],
    data: List[Any],
    name: str = "Algorithm",
    distribution: str = "random"
) -> Tuple[List[Any], SortMetrics]:
    """
    Executa um algoritmo de ordenação medindo tempo, comparações e movimentações.
    """
    data_copy = list(data)
    start = time.perf_counter()
    sorted_data, comparisons, moves = sort_fn(data_copy)
    elapsed = time.perf_counter() - start

    # Verificação de ordenação
    is_sorted = all(sorted_data[i] <= sorted_data[i + 1] for i in range(len(sorted_data) - 1))

    metrics = SortMetrics(
        algorithm_name=name,
        input_size=len(data),
        distribution=distribution,
        elapsed_time_sec=elapsed,
        comparisons=comparisons,
        swaps_or_moves=moves,
        is_sorted=is_sorted,
    )
    return sorted_data, metrics
