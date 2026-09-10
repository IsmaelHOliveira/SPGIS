#include "classical.hpp"
#include <algorithm>

SortResult bubble_sort(std::vector<int> arr) {
    SortResult res;
    res.data = std::move(arr);
    res.comparisons = 0;
    res.moves = 0;

    size_t n = res.data.size();
    if (n <= 1) return res;

    for (size_t i = 0; i < n; ++i) {
        bool swapped = false;
        for (size_t j = 0; j < n - i - 1; ++j) {
            res.comparisons++;
            if (res.data[j] > res.data[j + 1]) {
                std::swap(res.data[j], res.data[j + 1]);
                res.moves += 2;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
    return res;
}

SortResult selection_sort(std::vector<int> arr) {
    SortResult res;
    res.data = std::move(arr);
    res.comparisons = 0;
    res.moves = 0;

    size_t n = res.data.size();
    if (n <= 1) return res;

    for (size_t i = 0; i < n; ++i) {
        size_t min_idx = i;
        for (size_t j = i + 1; j < n; ++j) {
            res.comparisons++;
            if (res.data[j] < res.data[min_idx]) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            std::swap(res.data[i], res.data[min_idx]);
            res.moves += 2;
        }
    }
    return res;
}

SortResult insertion_sort(std::vector<int> arr) {
    SortResult res;
    res.data = std::move(arr);
    res.comparisons = 0;
    res.moves = 0;

    size_t n = res.data.size();
    if (n <= 1) return res;

    for (size_t i = 1; i < n; ++i) {
        int key = res.data[i];
        res.moves++;
        int64_t j = static_cast<int64_t>(i) - 1;
        while (j >= 0) {
            res.comparisons++;
            if (res.data[j] > key) {
                res.data[j + 1] = res.data[j];
                res.moves++;
                j--;
            } else {
                break;
            }
        }
        res.data[j + 1] = key;
        res.moves++;
    }
    return res;
}

static void merge_sort_rec(std::vector<int>& arr, std::vector<int>& temp,
                           size_t left, size_t right,
                           uint64_t& comps, uint64_t& moves) {
    if (left >= right) return;

    size_t mid = left + (right - left) / 2;
    merge_sort_rec(arr, temp, left, mid, comps, moves);
    merge_sort_rec(arr, temp, mid + 1, right, comps, moves);

    size_t i = left, j = mid + 1, k = left;
    while (i <= mid && j <= right) {
        comps++;
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
            moves++;
        } else {
            temp[k++] = arr[j++];
            moves++;
        }
    }
    while (i <= mid) {
        temp[k++] = arr[i++];
        moves++;
    }
    while (j <= right) {
        temp[k++] = arr[j++];
        moves++;
    }
    for (size_t idx = left; idx <= right; ++idx) {
        arr[idx] = temp[idx];
        moves++;
    }
}

SortResult merge_sort(std::vector<int> arr) {
    SortResult res;
    res.data = std::move(arr);
    res.comparisons = 0;
    res.moves = 0;

    if (res.data.size() <= 1) return res;

    std::vector<int> temp(res.data.size());
    merge_sort_rec(res.data, temp, 0, res.data.size() - 1, res.comparisons, res.moves);
    return res;
}

static void quick_sort_rec(std::vector<int>& arr, int64_t low, int64_t high,
                           uint64_t& comps, uint64_t& moves) {
    if (low >= high) return;

    int64_t mid = low + (high - low) / 2;
    // Median-of-three
    comps += 3;
    if (arr[low] > arr[mid]) { std::swap(arr[low], arr[mid]); moves += 2; }
    if (arr[low] > arr[high]) { std::swap(arr[low], arr[high]); moves += 2; }
    if (arr[mid] > arr[high]) { std::swap(arr[mid], arr[high]); moves += 2; }

    int pivot = arr[mid];
    int64_t i = low;
    int64_t j = high;

    while (i <= j) {
        while (true) {
            comps++;
            if (arr[i] < pivot) i++; else break;
        }
        while (true) {
            comps++;
            if (arr[j] > pivot) j--; else break;
        }
        if (i <= j) {
            if (i != j) {
                std::swap(arr[i], arr[j]);
                moves += 2;
            }
            i++;
            j--;
        }
    }

    if (low < j) quick_sort_rec(arr, low, j, comps, moves);
    if (i < high) quick_sort_rec(arr, i, high, comps, moves);
}

SortResult quick_sort(std::vector<int> arr) {
    SortResult res;
    res.data = std::move(arr);
    res.comparisons = 0;
    res.moves = 0;

    if (res.data.size() <= 1) return res;
    quick_sort_rec(res.data, 0, static_cast<int64_t>(res.data.size()) - 1, res.comparisons, res.moves);
    return res;
}
