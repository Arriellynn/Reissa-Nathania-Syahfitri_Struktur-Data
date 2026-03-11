"""
Soal 4 — Merge Tiga Sorted Lists
Implementasikan mergeThreeSortedLists(listA, listB, listC)
yang menggabungkan tiga sorted list menjadi satu sorted list baru
dalam waktu O(n) menggunakan SATU pass dengan tiga pointer.
(Tidak boleh memanggil fungsi merge dua list secara bertahap)
"""


def mergeThreeSortedLists(listA, listB, listC):
    """
    Menggabungkan tiga sorted list menjadi satu sorted list
    dalam satu pass menggunakan tiga pointer i, j, k.

    Kompleksitas waktu : O(n)  — n = len(A) + len(B) + len(C)
    Kompleksitas ruang : O(n)  — untuk list hasil
    """
    result = []
    i, j, k = 0, 0, 0
    a, b, c = len(listA), len(listB), len(listC)

    while i < a or j < b or k < c:
        # Gunakan inf jika pointer sudah habis
        va = listA[i] if i < a else float('inf')
        vb = listB[j] if j < b else float('inf')
        vc = listC[k] if k < c else float('inf')

        # Pilih nilai terkecil dari ketiga pointer
        if va <= vb and va <= vc:
            result.append(va)
            i += 1
        elif vb <= va and vb <= vc:
            result.append(vb)
            j += 1
        else:
            result.append(vc)
            k += 1

    return result


# --- Uji ---
if __name__ == "__main__":
    print("=" * 55)
    print("SOAL 4 — Merge Tiga Sorted Lists")
    print("=" * 55)

    # Contoh dari soal
    A = [1, 5, 9]
    B = [2, 6, 10]
    C = [3, 4, 7]
    hasil = mergeThreeSortedLists(A, B, C)
    print(f"\nInput :")
    print(f"  listA = {A}")
    print(f"  listB = {B}")
    print(f"  listC = {C}")
    print(f"\nmergeThreeSortedLists(listA, listB, listC)")
    print(f"→ {hasil}")

    # Uji tambahan
    print("\n--- Uji Tambahan ---")
    X = [1, 3, 5, 7]
    Y = [2, 4, 6]
    Z = [0, 8, 9, 10]
    hasil2 = mergeThreeSortedLists(X, Y, Z)
    print(f"listX = {X}")
    print(f"listY = {Y}")
    print(f"listZ = {Z}")
    print(f"→ {hasil2}")

    print("""
Penjelasan:
  Algoritma menggunakan tiga pointer (i, j, k) yang masing-masing
  menunjuk posisi saat ini di listA, listB, dan listC.
  Setiap iterasi, nilai terkecil dari ketiga pointer dipilih dan
  dimasukkan ke result, lalu pointer yang bersangkutan maju satu langkah.
  Jika salah satu list sudah habis, nilainya diganti inf agar tidak dipilih.
  Ini memastikan hanya SATU pass tanpa pemanggilan merge bertahap.
""")
