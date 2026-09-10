"""
Algoritmo Autoral de Referência: Dual-Pivot Extremes Sieve Sort (DPES).

Raciocínio Projetual:
1. Identifica em O(N) os extremos locais (mínimo e máximo).
2. Se min == max, o array possui todos os elementos idênticos -> encerra imediatamente em O(N).
3. Fixa min na extremidade esquerda e max na extremidade direita.
4. Calcula dois pivôs adaptativos por interpolação de faixa de valores (p1, p2).
5. Realiza particionamento triplo convergente in-place (esquerda, centro, direita).
6. Aplica Insertion Sort otimizado para partições de tamanho <= 16 (threshold de sobrecarga).
"""

from typing import Any, List, Tuple


def dpes_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Dual-Pivot Extremes Sieve Sort (DPES).
    
    Retorna:
        Tuple[List[Any], int, int]: (lista_ordenada, comparacoes, movimentacoes)
    """
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a, 0, 0

    comps = [0]
    moves = [0]
    INSERTION_THRESHOLD = 16

    def _insertion_sort(low: int, high: int) -> None:
        for i in range(low + 1, high + 1):
            key = a[i]
            moves[0] += 1
            j = i - 1
            while j >= low:
                comps[0] += 1
                if a[j] > key:
                    a[j + 1] = a[j]
                    moves[0] += 1
                    j -= 1
                else:
                    break
            a[j + 1] = key
            moves[0] += 1

    def _sort_recursive(low: int, high: int) -> None:
        if low >= high:
            return

        size = high - low + 1
        if size <= INSERTION_THRESHOLD:
            _insertion_sort(low, high)
            return

        # 1. Encontrar mínimo e máximo no intervalo
        min_idx = low
        max_idx = low
        for k in range(low + 1, high + 1):
            comps[0] += 1
            if a[k] < a[min_idx]:
                min_idx = k
            comps[0] += 1
            if a[k] > a[max_idx]:
                max_idx = k

        # Se todos os elementos do segmento forem iguais
        if a[min_idx] == a[max_idx]:
            comps[0] += 1
            return

        # 2. Posicionar min no início (low) e max no final (high)
        if min_idx != low:
            a[low], a[min_idx] = a[min_idx], a[low]
            moves[0] += 2
            # Se o max_idx era o low original, atualiza o índice do max
            if max_idx == low:
                max_idx = min_idx

        if max_idx != high:
            a[high], a[max_idx] = a[max_idx], a[high]
            moves[0] += 2

        min_val = a[low]
        max_val = a[high]

        # 3. Interpolação adaptativa de pivôs (se numérico) ou mediana empírica
        try:
            span = max_val - min_val
            p1 = min_val + span / 3
            p2 = min_val + (2 * span) / 3
        except TypeError:
            # Fallback para elementos não aritméticos: seleção posicional
            mid = low + size // 2
            comps[0] += 1
            if a[low] > a[mid]:
                p1, p2 = a[mid], a[low]
            else:
                p1, p2 = a[low], a[mid]

        # 4. Particionamento tripartite in-place no intervalo [low + 1, high - 1]
        left = low + 1
        curr = low + 1
        right = high - 1

        while curr <= right:
            comps[0] += 1
            if a[curr] < p1:
                if curr != left:
                    a[curr], a[left] = a[left], a[curr]
                    moves[0] += 2
                left += 1
                curr += 1
            else:
                comps[0] += 1
                if a[curr] > p2:
                    while curr < right:
                        comps[0] += 1
                        if a[right] > p2:
                            right -= 1
                        else:
                            break
                    if curr != right:
                        a[curr], a[right] = a[right], a[curr]
                        moves[0] += 2
                    right -= 1

                    # Reavalia o elemento trazido de right
                    comps[0] += 1
                    if a[curr] < p1:
                        if curr != left:
                            a[curr], a[left] = a[left], a[curr]
                            moves[0] += 2
                        left += 1
                curr += 1

        # 5. Chamadas recursivas para as 3 partições
        _sort_recursive(low, left - 1)
        _sort_recursive(left, right)
        _sort_recursive(right + 1, high)

    _sort_recursive(0, n - 1)
    return a, comps[0], moves[0]
