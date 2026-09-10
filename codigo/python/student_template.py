"""
TEMPLATE PARA O ALUNO — TRABALHO PRÁTICO 1 (TP1)
Disciplina: Análise e Projetos de Algoritmos (APA)

Instruções:
1. Implemente seu método de ordenação autoral na função `my_authorial_sort`.
2. O retorno deve ser obrigatoriamente a tupla: (lista_ordenada, total_comparacoes, total_movimentacoes).
3. Execute este arquivo diretamente para rodar a suíte de testes de corretude e o benchmark rápido.
"""

from typing import Any, List, Tuple
import unittest


def my_authorial_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    IMPLEMENTE AQUI SEU ALGORITMO AUTORAL.

    Parâmetros:
        arr (List[Any]): Lista de entrada a ser ordenada.

    Retorno:
        Tuple[List[Any], int, int]:
            - Lista ordenada
            - Total de comparações realizadas
            - Total de movimentações/trocas realizadas
    """
    a = list(arr)
    n = len(a)
    comps = 0
    moves = 0

    # =========================================================================
    # TODO: Escreva sua lógica autoral aqui.
    # Exemplo temporário (substitua pelo seu algoritmo):
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
    # =========================================================================

    return a, comps, moves


# =============================================================================
# SUÍTE DE TESTES AUTOMÁTICA DE VALIDAÇÃO
# =============================================================================
class TestStudentAuthorialSort(unittest.TestCase):
    def assert_sorted(self, original: List, result: List):
        self.assertEqual(len(result), len(original), "Tamanho divergente!")
        self.assertEqual(sorted(original), result, "A lista não foi ordenada corretamente!")

    def test_empty(self):
        res, _, _ = my_authorial_sort([])
        self.assert_sorted([], res)

    def test_single(self):
        res, _, _ = my_authorial_sort([99])
        self.assert_sorted([99], res)

    def test_sorted(self):
        data = list(range(100))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_reverse(self):
        data = list(range(100, 0, -1))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_identical(self):
        data = [5] * 50
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_random(self):
        import random
        random.seed(42)
        data = [random.randint(-1000, 1000) for _ in range(200)]
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)


if __name__ == "__main__":
    print("🧪 Executando testes unitários no seu algoritmo autoral...")
    unittest.main(verbosity=2)
