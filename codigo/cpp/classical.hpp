#ifndef CLASSICAL_SORT_HPP
#define CLASSICAL_SORT_HPP

#include <vector>
#include <cstdint>

struct SortResult {
    std::vector<int> data;
    uint64_t comparisons;
    uint64_t moves;
};

// Algoritmos clássicos instrumentados
SortResult bubble_sort(std::vector<int> arr);
SortResult selection_sort(std::vector<int> arr);
SortResult insertion_sort(std::vector<int> arr);
SortResult merge_sort(std::vector<int> arr);
SortResult quick_sort(std::vector<int> arr);

#endif // CLASSICAL_SORT_HPP
