import math
from typing import List, Optional


class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class AdvancedSorter:
    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # =========================================================

    def sort_array(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        tmp_array = [0] * len(arr)  # Single temporary array, allocated once
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        if first >= last:
            return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        """
        Menggabungkan dua virtual sublist yang bersebelahan.
        Menggunakan tmp_array sebagai penyimpanan sementara (STABLE).
        """
        a = left_start
        b = mid + 1
        k = left_start

        while a <= mid and b <= right_end:
            # Gunakan <= agar STABLE: elemen kiri diprioritaskan jika sama
            if arr[a] <= arr[b]:
                tmp_array[k] = arr[a]
                a += 1
            else:
                tmp_array[k] = arr[b]
                b += 1
            k += 1

        # Salin sisa elemen kiri
        while a <= mid:
            tmp_array[k] = arr[a]
            a += 1
            k += 1

        # Salin sisa elemen kanan
        while b <= right_end:
            tmp_array[k] = arr[b]
            b += 1
            k += 1

        # Salin kembali dari tmp_array ke arr
        for i in range(left_start, right_end + 1):
            arr[i] = tmp_array[i]

    # =========================================================
    # 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)
    # =========================================================

    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        right_head = self._split_linked_list(head)
        left_head = head

        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)

        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """
        Menemukan titik tengah dengan fast-slow pointer dalam satu traversal.
        midPoint bergerak 1 langkah, curNode bergerak 2 langkah.
        """
        mid_point = head
        cur_node = head.next

        while cur_node is not None and cur_node.next is not None:
            mid_point = mid_point.next
            cur_node = cur_node.next.next

        # Putus linked list menjadi dua bagian
        right_head = mid_point.next
        mid_point.next = None

        return right_head

    def _merge_linked_lists(self, listA: Optional[ListNode], listB: Optional[ListNode]) -> Optional[ListNode]:
        """
        Menggabungkan dua sorted linked list menggunakan dummy node & tail reference.
        Tidak mengalokasi node baru — hanya memodifikasi pointer .next (STABLE).
        """
        dummy = ListNode(0)  # Dummy node statis sebagai sentinel
        tail = dummy

        while listA is not None and listB is not None:
            # Gunakan <= agar STABLE
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail = tail.next

        # Sambungkan sisa list yang belum habis
        tail.next = listA if listA is not None else listB

        return dummy.next

    # =========================================================
    # 3. QUICK SORT (Median-of-Three Pivot + Depth Fallback)
    # =========================================================

    def sort_quick(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        max_depth = int(2 * math.log2(len(arr)))
        self._quick_sort_recursive(arr, 0, len(arr) - 1, max_depth, 0)
        return arr

    def _quick_sort_recursive(self, arr, first, last, max_depth, depth):
        if first >= last:
            return

        # Fallback ke merge sort jika kedalaman rekursi melebihi batas
        if depth > max_depth:
            sub = arr[first:last + 1]
            self.sort_array(sub)
            arr[first:last + 1] = sub
            return

        pivot_pos = self.partition_quick(arr, first, last)
        self._quick_sort_recursive(arr, first, pivot_pos - 1, max_depth, depth + 1)
        self._quick_sort_recursive(arr, pivot_pos + 1, last, max_depth, depth + 1)

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """
        Memilih pivot menggunakan Median-of-Three (first, mid, last).
        Tukar pivot ke posisi 'first', lalu jalankan partisi in-place.
        Catatan: Partisi ini tidak sepenuhnya stable karena swap elemen jauh,
        namun pivot median-of-three mencegah worst-case O(n^2).
        """
        mid = (first + last) // 2

        # Urutkan arr[first], arr[mid], arr[last] untuk temukan median
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]
        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]

        # arr[mid] sekarang adalah median — tukar ke posisi first sebagai pivot
        arr[first], arr[mid] = arr[mid], arr[first]
        pivot = arr[first]

        left = first + 1
        right = last

        while left <= right:
            while left <= right and arr[left] <= pivot:
                left += 1
            while left <= right and arr[right] > pivot:
                right -= 1
            if left < right:
                arr[left], arr[right] = arr[right], arr[left]

        # Tempatkan pivot di posisi akhirnya
        arr[first], arr[right] = arr[right], arr[first]

        return right


# =========================================================
# TEST CASES
# =========================================================

def linked_list_to_str(head):
    result = []
    while head:
        result.append(str(head.data))
        head = head.next
    return " -> ".join(result)


def build_linked_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    cur = head
    for v in values[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


if __name__ == "__main__":
    sorter = AdvancedSorter()

    print("=" * 50)
    print("ARRAY MERGE SORT")
    print("=" * 50)
    arr1 = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print(f"Input:  {arr1}")
    result1 = sorter.sort_array(arr1)
    print(f"Output: {result1}")

    print()
    arr2 = [3, 3, 1, 1, 2, 2]  # Test stabilitas
    print(f"Input (duplikat): {arr2}")
    result2 = sorter.sort_array(arr2)
    print(f"Output: {result2}")

    print()
    print("=" * 50)
    print("LINKED LIST MERGE SORT")
    print("=" * 50)
    ll1 = build_linked_list([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"Input:  {linked_list_to_str(ll1)}")
    sorted_ll = sorter.sort_linked_list(ll1)
    print(f"Output: {linked_list_to_str(sorted_ll)}")

    print()
    print("=" * 50)
    print("QUICK SORT (Median-of-Three)")
    print("=" * 50)
    arr3 = [9, 8, 7, 6, 5, 4, 3, 2, 1]  # Worst-case descending
    print(f"Input (descending): {arr3}")
    result3 = sorter.sort_quick(arr3)
    print(f"Output: {result3}")

    print()
    arr4 = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Already sorted
    print(f"Input (ascending):  {arr4}")
    result4 = sorter.sort_quick(arr4)
    print(f"Output: {result4}")
