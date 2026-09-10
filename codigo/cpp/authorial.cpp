#include "authorial.hpp"
#include <algorithm>

constexpr int64_t INSERTION_THRESHOLD = 16;

static void insertion_sort_range(std::vector<int>& a, int64_t low, int64_t high,
                                 uint64_t& comps, uint64_t& moves) {
    for (int64_t i = low + 1; i <= high; ++i) {
        int key = a[i];
        moves++;
        int64_t j = i - 1;
        while (j >= low) {
            comps++;
            if (a[j] > key) {
                a[j + 1] = a[j];
                moves++;
                j--;
            } else {
                break;
            }
        }
        a[j + 1] = key;
        moves++;
    }
}

static void dpes_rec(std::vector<int>& a, int64_t low, int64_t high,
                     uint64_t& comps, uint64_t& moves) {
    if (low >= high) return;

    int64_t size = high - low + 1;
    if (size <= INSERTION_THRESHOLD) {
        insertion_sort_range(a, low, high, comps, moves);
        return;
    }

    // 1. Encontra extremos mínimo e máximo no intervalo
    int64_t min_idx = low;
    int64_t max_idx = low;
    for (int64_t k = low + 1; k <= high; ++k) {
        comps++;
        if (a[k] < a[min_idx]) min_idx = k;
        comps++;
        if (a[k] > a[max_idx]) max_idx = k;
    }

    // Caso de elementos todos idênticos
    if (a[min_idx] == a[max_idx]) {
        comps++;
        return;
    }

    // 2. Posiciona min no início e max no final
    if (min_idx != low) {
        std::swap(a[low], a[min_idx]);
        moves += 2;
        if (max_idx == low) max_idx = min_idx;
    }
    if (max_idx != high) {
        std::swap(a[high], a[max_idx]);
        moves += 2;
    }

    int min_val = a[low];
    int max_val = a[high];

    // 3. Interpolação adaptativa de pivôs
    int64_t span = static_cast<int64_t>(max_val) - static_cast<int64_t>(min_val);
    int p1 = min_val + static_cast<int>(span / 3);
    int p2 = min_val + static_cast<int>((2 * span) / 3);

    // 4. Particionamento tripartite convergente in-place
    int64_t left = low + 1;
    int64_t curr = low + 1;
    int64_t right = high - 1;

    while (curr <= right) {
        comps++;
        if (a[curr] < p1) {
            if (curr != left) {
                std::swap(a[curr], a[left]);
                moves += 2;
            }
            left++;
            curr++;
        } else {
            comps++;
            if (a[curr] > p2) {
                while (curr < right) {
                    comps++;
                    if (a[right] > p2) right--;
                    else break;
                }
                if (curr != right) {
                    std::swap(a[curr], a[right]);
                    moves += 2;
                }
                right--;

                comps++;
                if (a[curr] < p1) {
                    if (curr != left) {
                        std::swap(a[curr], a[left]);
                        moves += 2;
                    }
                    left++;
                }
            }
            curr++;
        }
    }

    // 5. Recursão para as 3 partições
    dpes_rec(a, low, left - 1, comps, moves);
    dpes_rec(a, left, right, comps, moves);
    dpes_rec(a, right + 1, high, comps, moves);
}

SortResult dpes_sort(std::vector<int> arr) {
    SortResult res;
    res.data = std::move(arr);
    res.comparisons = 0;
    res.moves = 0;

    if (res.data.size() <= 1) return res;
    dpes_rec(res.data, 0, static_cast<int64_t>(res.data.size()) - 1, res.comparisons, res.moves);
    return res;
}
