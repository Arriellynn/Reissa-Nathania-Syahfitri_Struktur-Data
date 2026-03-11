"""
Soal 1 — Modified Binary Search
Implementasikan fungsi countOccurrences(sortedList, target)
yang menghitung berapa kali sebuah nilai muncul dalam sorted list.
Kompleksitas waktu: O(log n)
"""


def countOccurrences(sortedList, target):
    """
    Menghitung berapa kali 'target' muncul dalam sorted list.
    Menggunakan dua kali binary search:
      - findLeft  → indeks pertama kemunculan target
      - findRight → indeks terakhir kemunculan target
    Kompleksitas waktu: O(log n)
    """

    def findLeft(arr, t):
        lo, hi, result = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == t:
                result = mid
                hi = mid - 1      # terus cari ke kiri
            elif arr[mid] < t:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    def findRight(arr, t):
        lo, hi, result = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == t:
                result = mid
                lo = mid + 1      # terus cari ke kanan
            elif arr[mid] < t:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    left = findLeft(sortedList, target)
    if left == -1:
        return 0                  # target tidak ditemukan
    right = findRight(sortedList, target)
    return right - left + 1


# --- Uji ---
if __name__ == "__main__":
    list1 = [1, 2, 4, 4, 4, 4, 7, 9, 12]

    print("=" * 50)
    print("SOAL 1 — Modified Binary Search")
    print("=" * 50)
    print(f"List : {list1}")
    print()
    print(f"countOccurrences({list1}, 4) → {countOccurrences(list1, 4)}")  # 4
    print(f"countOccurrences({list1}, 5) → {countOccurrences(list1, 5)}")  # 0
