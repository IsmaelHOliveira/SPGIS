"""
Implementação dos Algoritmos Clássicos de Ordenação da Literatura.
Cada função retorna (lista_ordenada, comparacoes, movimentacoes).
"""

from typing import Any, List, Tuple


def bubble_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Bubble Sort com otimização de parada antecipada.
    Complexidade: Melhor O(n), Pior O(n²), Médio O(n²).
    Estabilidade: Estável.
    """
    a = list(arr)
    n = len(a)
    comps = 0
    moves = 0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                moves += 2
                swapped = True
        if not swapped:
            break

    return a, comps, moves


def selection_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Selection Sort.
    Complexidade: Melhor O(n²), Pior O(n²), Médio O(n²).
    Estabilidade: Não estável (versão in-place com trocas).
    """
    a = list(arr)
    n = len(a)
    comps = 0
    moves = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            moves += 2

    return a, comps, moves


def insertion_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Insertion Sort linear.
    Complexidade: Melhor O(n), Pior O(n²), Médio O(n²).
    Estabilidade: Estável.
    """
    a = list(arr)
    n = len(a)
    comps = 0
    moves = 0

    for i in range(1, n):
        key = a[i]
        moves += 1
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                moves += 1
                j -= 1
            else:
                break
        a[j + 1] = key
        moves += 1

    return a, comps, moves


def merge_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Merge Sort clássico (Divisão e Conquista).
    Complexidade: Melhor O(n log n), Pior O(n log n), Médio O(n log n).
    Espaço auxiliar: O(n).
    Estabilidade: Estável.
    """
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a, 0, 0

    comps = [0]
    moves = [0]

    def _merge_sort_rec(lst: List[Any]) -> List[Any]:
        if len(lst) <= 1:
            return lst

        mid = len(lst) // 2
        left = _merge_sort_rec(lst[:mid])
        right = _merge_sort_rec(lst[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comps[0] += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                moves[0] += 1
                i += 1
            else:
                merged.append(right[j])
                moves[0] += 1
                j += 1

        while i < len(left):
            merged.append(left[i])
            moves[0] += 1
            i += 1

        while j < len(right):
            merged.append(right[j])
            moves[0] += 1
            j += 1

        return merged

    result = _merge_sort_rec(a)
    return result, comps[0], moves[0]


def quick_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Quick Sort com partição de Hoare e escolha de pivô mediana de três.
    Complexidade: Melhor O(n log n), Pior O(n²), Médio O(n log n).
    Estabilidade: Não estável.
    """
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a, 0, 0

    comps = [0]
    moves = [0]

    def _median_of_three(low: int, high: int) -> int:
        mid = (low + high) // 2
        comps[0] += 3
        if a[low] > a[mid]:
            a[low], a[mid] = a[mid], a[low]
            moves[0] += 2
        if a[low] > a[high]:
            a[low], a[high] = a[high], a[low]
            moves[0] += 2
        if a[mid] > a[high]:
            a[mid], a[high] = a[high], a[mid]
            moves[0] += 2
        return mid

    def _quick_sort_rec(low: int, high: int) -> None:
        if low >= high:
            return

        # Mediana de 3 para seleção de pivô robusta
        pivot_idx = _median_of_three(low, high)
        pivot = a[pivot_idx]

        i = low
        j = high

        while i <= j:
            while True:
                comps[0] += 1
                if a[i] < pivot:
                    i += 1
                else:
                    break
            while True:
                comps[0] += 1
                if a[j] > pivot:
                    j -= 1
                else:
                    break
            if i <= j:
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    moves[0] += 2
                i += 1
                j -= 1

        if low < j:
            _quick_sort_rec(low, j)
        if i < high:
            _quick_sort_rec(i, high)

    _quick_sort_rec(0, n - 1)
    return a, comps[0], moves[0]
