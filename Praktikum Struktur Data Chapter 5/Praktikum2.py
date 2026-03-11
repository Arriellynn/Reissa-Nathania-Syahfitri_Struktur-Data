"""
Soal 2 — Bubble Sort dengan Analisis Langkah
Modifikasi bubbleSort() agar:
  - Mengembalikan tuple (sorted_list, total_comparisons, total_swaps, passes_used)
  - Mengimplementasikan early termination (berhenti jika tidak ada swap dalam satu pass)
  - Mencetak state array setelah setiap pass
"""


def bubbleSort(arr):
    """
    Bubble sort dengan early termination.
    Mengembalikan:
        sorted_list       – list yang sudah terurut
        total_comparisons – total perbandingan elemen
        total_swaps       – total pertukaran elemen
        passes_used       – jumlah pass yang benar-benar digunakan
    Mencetak state array setelah setiap pass.
    """
    data = arr[:]
    n = len(data)
    total_comparisons = 0
    total_swaps = 0
    passes_used = 0

    for pass_num in range(1, n):
        swapped = False
        for i in range(n - pass_num):
            total_comparisons += 1
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                total_swaps += 1
                swapped = True
        passes_used += 1
        print(f"  Pass {pass_num}: {data}")
        if not swapped:           # early termination
            break

    return data, total_comparisons, total_swaps, passes_used


# --- Uji ---
if __name__ == "__main__":
    print("=" * 50)
    print("SOAL 2 — Bubble Sort dengan Analisis Langkah")
    print("=" * 50)

    test_cases = [
        [5, 1, 4, 2, 8],
        [1, 2, 3, 4, 5],
    ]

    for test_input in test_cases:
        print(f"\nInput : {test_input}")
        sorted_list, comps, swaps, passes = bubbleSort(test_input)
        print(f"Output: {sorted_list}")
        print(f"  total_comparisons = {comps}")
        print(f"  total_swaps       = {swaps}")
        print(f"  passes_used       = {passes}")

    print("""
Penjelasan perbedaan jumlah pass:
  [5,1,4,2,8] → tidak terurut, banyak swap terjadi → perlu lebih banyak pass.
  [1,2,3,4,5] → sudah terurut sejak awal, pass pertama tidak ada swap
                → early termination langsung berhenti setelah 1 pass.
""")
