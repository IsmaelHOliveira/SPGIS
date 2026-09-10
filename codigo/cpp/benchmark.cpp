#include "classical.hpp"
#include "authorial.hpp"
#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <iomanip>
#include <string>
#include <functional>

struct BenchmarkResult {
    std::string alg_name;
    int size;
    std::string dist;
    double time_ms;
    uint64_t comparisons;
    uint64_t moves;
};

std::vector<int> make_dataset(int n, const std::string& dist, std::mt19937& rng) {
    std::vector<int> v(n);
    if (dist == "random") {
        for (int i = 0; i < n; ++i) v[i] = rng() % (10 * n);
    } else if (dist == "sorted") {
        for (int i = 0; i < n; ++i) v[i] = i;
    } else if (dist == "reverse") {
        for (int i = 0; i < n; ++i) v[i] = n - i;
    } else if (dist == "duplicates") {
        for (int i = 0; i < n; ++i) v[i] = rng() % 5;
    } else if (dist == "almost_sorted") {
        for (int i = 0; i < n; ++i) v[i] = i;
        int swaps = std::max(1, n / 20);
        for (int s = 0; s < swaps; ++s) {
            int i = rng() % n;
            int j = rng() % n;
            std::swap(v[i], v[j]);
        }
    }
    return v;
}

void benchmark_dist(const std::string& dist, const std::vector<int>& sizes) {
    std::cout << "\n### Distribuição: `" << dist << "` (C++ - Tempo em ms e Comparações)" << std::endl;
    std::cout << "| Algoritmo | " ;
    for (int s : sizes) std::cout << "N=" << s << " | ";
    std::cout << "\n| :--- | ";
    for (size_t i = 0; i < sizes.size(); ++i) std::cout << ":---: | ";
    std::cout << std::endl;

    std::vector<std::pair<std::string, std::function<SortResult(std::vector<int>)>>> algs = {
        {"Bubble Sort", bubble_sort},
        {"Selection Sort", selection_sort},
        {"Insertion Sort", insertion_sort},
        {"Merge Sort", merge_sort},
        {"Quick Sort", quick_sort},
        {"Authorial (DPES)", dpes_sort}
    };

    std::mt19937 rng(42);

    for (const auto& alg : algs) {
        std::cout << "| " << alg.first << " | ";
        for (int s : sizes) {
            if (s > 2000 && (alg.first == "Bubble Sort" || alg.first == "Selection Sort" || alg.first == "Insertion Sort") && (dist == "random" || dist == "reverse")) {
                std::cout << "— | ";
                continue;
            }

            int trials = 3;
            double total_time = 0.0;
            for (int t = 0; t < trials; ++t) {
                auto data = make_dataset(s, dist, rng);
                auto start = std::chrono::high_resolution_clock::now();
                auto res = alg.second(data);
                auto end = std::chrono::high_resolution_clock::now();
                total_time += std::chrono::duration<double, std::milli>(end - start).count();
            }
            double avg_ms = total_time / trials;
            std::cout << std::fixed << std::setprecision(3) << avg_ms << " ms | ";
        }
        std::cout << std::endl;
    }
}

int main() {
    std::vector<int> sizes = {10, 50, 100, 250, 500, 1000, 2500};
    std::vector<std::string> dists = {"random", "sorted", "reverse", "duplicates", "almost_sorted"};

    std::cout << "# Resultados dos Benchmarks em C++ — APA (TP1)" << std::endl;
    for (const auto& d : dists) {
        benchmark_dist(d, sizes);
    }
    return 0;
}
