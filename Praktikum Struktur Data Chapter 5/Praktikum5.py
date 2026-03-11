"""
Soal 5 — Inversions Counter
Sebuah inversion dalam array adalah pasangan indeks (i, j)
dimana i < j tapi arr[i] > arr[j].

a) countInversionsNaive(arr)  — brute force O(n²)
b) countInversionsSmart(arr) — modifikasi merge sort O(n log n)

Uji kedua fungsi, pastikan hasilnya sama, dan ukur waktu eksekusi
pada array random berukuran 1000, 5000, dan 10000.
"""

import time
import random


# ── a) Brute Force O(n²) ─────────────────────────────────────

def countInversionsNaive(arr):
    """
    Hitung inversion dengan brute force.
    Periksa semua pasangan (i, j) dimana i < j.
    Kompleksitas: O(n²)
    """
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


# ── b) Merge Sort O(n log n) ──────────────────────────────────

def countInversionsSmart(arr):
    """
    Hitung inversion menggunakan modifikasi merge sort.
    Saat merge: jika elemen kanan < elemen kiri,
    maka semua elemen sisa di sisi kiri adalah inversion
    → tambahkan (mid - i + 1) ke count.
    Kompleksitas: O(n log n)
    """

    def mergeCount(arr, temp, lo, hi):
        if lo >= hi:
            return 0
        mid = (lo + hi) // 2
        count  = mergeCount(arr, temp, lo, mid)
        count += mergeCount(arr, temp, mid + 1, hi)
        count += merge(arr, temp, lo, mid, hi)
        return count

    def merge(arr, temp, lo, mid, hi):
        # Salin ke array sementara
        for idx in range(lo, hi + 1):
            temp[idx] = arr[idx]

        i, j, k = lo, mid + 1, lo
        inv = 0

        while i <= mid and j <= hi:
            if temp[i] <= temp[j]:
                arr[k] = temp[i]
                i += 1
            else:
                # temp[i..mid] semuanya lebih besar dari temp[j]
                inv += (mid - i + 1)
                arr[k] = temp[j]
                j += 1
            k += 1

        while i <= mid:
            arr[k] = temp[i]
            i += 1
            k += 1

        while j <= hi:
            arr[k] = temp[j]
            j += 1
            k += 1

        return inv

    data = arr[:]
    temp = [0] * len(data)
    return mergeCount(data, temp, 0, len(data) - 1)


# --- Uji ---
if __name__ == "__main__":
    print("=" * 55)
    print("SOAL 5 — Inversions Counter")
    print("=" * 55)

    # Verifikasi kesamaan hasil
    sample = [3, 1, 2, 5, 4]
    naive  = countInversionsNaive(sample)
    smart  = countInversionsSmart(sample)
    print(f"\nArray contoh : {sample}")
    print(f"Naive  result: {naive}")
    print(f"Smart  result: {smart}")
    print(f"Hasil sama   : {naive == smart}")

    # Inversions yang ada: (3,1), (3,2), (5,4) → 3 inversion

    # Ukur waktu eksekusi
    print(f"\n{'Ukuran':>8}  {'Naive (s)':>12}  {'Smart (s)':>12}  {'Inv Count':>12}")
    print("-" * 52)

    for size in [1000, 5000, 10000]:
        data = [random.randint(1, 100_000) for _ in range(size)]

        t0 = time.perf_counter()
        inv_naive = countInversionsNaive(data)
        t_naive = time.perf_counter() - t0

        t0 = time.perf_counter()
        inv_smart = countInversionsSmart(data)
        t_smart = time.perf_counter() - t0

        assert inv_naive == inv_smart, "ERROR: Hasil berbeda!"
        print(f"{size:>8}  {t_naive:>12.4f}  {t_smart:>12.6f}  {inv_naive:>12}")

    print("""
Penjelasan mengapa merge sort lebih cepat:
  - Naive  O(n²)     : untuk n=10000 → ~50 juta perbandingan.
  - Smart  O(n log n): untuk n=10000 → hanya ~130.000 operasi.

  Kunci optimasi merge sort:
  Ketika elemen kanan (temp[j]) lebih kecil dari elemen kiri (temp[i])
  saat proses merge, maka SEMUA elemen yang tersisa di sisi kiri
  (temp[i..mid]) pasti lebih besar dari temp[j].
  Jumlah inversion yang ditambahkan sekaligus = (mid - i + 1),
  tanpa perlu iterasi tambahan — inilah yang membuat Smart O(n log n).
""")
