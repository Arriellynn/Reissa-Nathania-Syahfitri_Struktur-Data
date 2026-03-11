"""
Soal 3 — Hybrid Sort
Buat fungsi hybridSort(theSeq, threshold=10) yang menggunakan:
  - Insertion sort jika panjang sub-array <= threshold
  - Selection sort jika panjang sub-array > threshold
Bandingkan jumlah total operasi (comparisons + swaps) antara
hybrid sort, pure insertion sort, dan pure selection sort
pada array random berukuran 50, 100, dan 500 elemen.
"""

import random


# ── Hybrid Sort ──────────────────────────────────────────────

def hybridSort(theSeq, threshold=10):
    """
    Hybrid sort dengan penghitungan operasi.
    Mengembalikan (sorted_list, total_operations).
    """
    arr = list(theSeq)
    ops = [0]

    def _insertionSort(a, lo, hi):
        for i in range(lo + 1, hi + 1):
            key = a[i]
            j = i - 1
            while j >= lo and a[j] > key:
                ops[0] += 2       # 1 comparison + 1 shift
                a[j + 1] = a[j]
                j -= 1
            ops[0] += 1           # comparison terakhir yang menghentikan loop
            a[j + 1] = key

    def _selectionSort(a, lo, hi):
        for i in range(lo, hi + 1):
            min_idx = i
            for j in range(i + 1, hi + 1):
                ops[0] += 1       # comparison
                if a[j] < a[min_idx]:
                    min_idx = j
            if min_idx != i:
                ops[0] += 1       # swap
                a[i], a[min_idx] = a[min_idx], a[i]

    length = len(arr)
    if length <= 1:
        return arr, 0

    if length <= threshold:
        _insertionSort(arr, 0, length - 1)
    else:
        _selectionSort(arr, 0, length - 1)

    return arr, ops[0]


# ── Pure Insertion Sort ───────────────────────────────────────

def pureInsertionSort(theSeq):
    arr = list(theSeq)
    ops = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            ops += 2
            arr[j + 1] = arr[j]
            j -= 1
        ops += 1
        arr[j + 1] = key
    return arr, ops


# ── Pure Selection Sort ───────────────────────────────────────

def pureSelectionSort(theSeq):
    arr = list(theSeq)
    ops = 0
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            ops += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            ops += 1
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr, ops


# --- Uji ---
if __name__ == "__main__":
    print("=" * 55)
    print("SOAL 3 — Hybrid Sort")
    print("=" * 55)
    print(f"\n{'Ukuran':>8}  {'Hybrid':>10}  {'Insertion':>10}  {'Selection':>10}")
    print("-" * 45)

    for size in [50, 100, 500]:
        data = [random.randint(1, 1000) for _ in range(size)]
        _, h_ops = hybridSort(data, threshold=10)
        _, i_ops = pureInsertionSort(data)
        _, s_ops = pureSelectionSort(data)
        print(f"{size:>8}  {h_ops:>10}  {i_ops:>10}  {s_ops:>10}")

    print("""
Catatan:
  - Untuk array kecil (≤ threshold), Insertion Sort lebih efisien
    karena memanfaatkan urutan parsial yang sudah ada.
  - Untuk array besar (> threshold), Selection Sort digunakan
    dan jumlah swaps-nya minimal (paling banyak n-1 swap).
  - Hybrid Sort menggabungkan keunggulan keduanya sesuai ukuran.
""")
