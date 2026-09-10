#include "classical.hpp"
#include "authorial.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <cassert>
#include <functional>
#include <string>

void run_test_suite(const std::string& alg_name, const std::function<SortResult(std::vector<int>)>& sort_fn) {
    std::cout << "  🧪 Testando [" << alg_name << "]...";

    // 1. Vetor vazio
    {
        std::vector<int> v = {};
        auto res = sort_fn(v);
        assert(res.data.empty());
    }

    // 2. Elemento único
    {
        std::vector<int> v = {42};
        auto res = sort_fn(v);
        assert(res.data.size() == 1 && res.data[0] == 42);
    }

    // 3. Já ordenado
    {
        std::vector<int> v(100);
        for (int i = 0; i < 100; ++i) v[i] = i;
        auto expected = v;
        auto res = sort_fn(v);
        assert(res.data == expected);
    }

    // 4. Inversamente ordenado
    {
        std::vector<int> v(100);
        for (int i = 0; i < 100; ++i) v[i] = 100 - i;
        auto expected = v;
        std::sort(expected.begin(), expected.end());
        auto res = sort_fn(v);
        assert(res.data == expected);
    }

    // 5. Elementos idênticos
    {
        std::vector<int> v(50, 7);
        auto res = sort_fn(v);
        assert(res.data == v);
    }

    // 6. Muitos repetidos
    {
        std::mt19937 rng(42);
        std::vector<int> v(200);
        for (auto& x : v) x = rng() % 5;
        auto expected = v;
        std::sort(expected.begin(), expected.end());
        auto res = sort_fn(v);
        assert(res.data == expected);
    }

    // 7. Números negativos
    {
        std::vector<int> v = {-50, 10, -200, 0, 5, -1, 100, -50};
        auto expected = v;
        std::sort(expected.begin(), expected.end());
        auto res = sort_fn(v);
        assert(res.data == expected);
    }

    // 8. Aleatório grande
    {
        std::mt19937 rng(123);
        std::vector<int> v(1000);
        for (auto& x : v) x = static_cast<int>(rng() % 20000) - 10000;
        auto expected = v;
        std::sort(expected.begin(), expected.end());
        auto res = sort_fn(v);
        assert(res.data == expected);
    }

    std::cout << " [PASSOU EM TODOS OS CENÁRIOS ✅]" << std::endl;
}

int main() {
    std::cout << "==================================================" << std::endl;
    std::cout << "  SUÍTE DE TESTES UNITÁRIOS EM C++ — APA (TP1)    " << std::endl;
    std::cout << "==================================================" << std::endl;

    run_test_suite("Bubble Sort", bubble_sort);
    run_test_suite("Selection Sort", selection_sort);
    run_test_suite("Insertion Sort", insertion_sort);
    run_test_suite("Merge Sort", merge_sort);
    run_test_suite("Quick Sort", quick_sort);
    run_test_suite("Authorial (DPES)", dpes_sort);

    std::cout << "\n🎉 Todos os 6 algoritmos foram validados com 100% de sucesso no C++!" << std::endl;
    return 0;
}
