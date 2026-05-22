from typing import List, Optional
from collections import deque


class ExprHeapSorter:
    def __init__(self, expr_str: str):
        self.expr = expr_str
        self.values = []

    # =========================================================
    # 1. EXPRESSION TREE BUILDER & EVALUATOR
    # =========================================================

    def parse_and_evaluate(self) -> List[int]:
        """Membangun pohon ekspresi, mengevaluasi, mengembalikan list nilai integer."""
        # Tokenisasi: pisahkan karakter bermakna, abaikan spasi
        tokens = deque()
        i = 0
        expr = self.expr.replace(" ", "")
        while i < len(expr):
            ch = expr[i]
            if ch in "()+-*/":
                tokens.append(ch)
                i += 1
            elif ch.isdigit() or (ch == '-' and i + 1 < len(expr) and expr[i + 1].isdigit()):
                # Tangani bilangan multi-digit
                j = i + 1
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                tokens.append(expr[i:j])
                i = j
            else:
                raise ValueError(f"Token tidak valid: '{ch}'")

        root = self._build_tree(tokens)
        result = self._eval_tree(root)
        self.values = [int(result)]
        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Membangun pohon ekspresi secara rekursif dari antrian token.
        Pola: '(' -> bangun kiri -> operator -> bangun kanan -> ')' diabaikan.
        Operand langsung di-assign dan return.
        """
        if not tokens:
            return None

        token = tokens.popleft()

        if token == '(':
            # Bangun subtree kiri
            left = self._build_tree(tokens)

            # Ambil operator
            if not tokens:
                raise ValueError("Ekspresi tidak lengkap: operator hilang")
            operator = tokens.popleft()
            if operator not in "+-*/":
                raise ValueError(f"Operator tidak valid: '{operator}'")

            # Bangun subtree kanan
            right = self._build_tree(tokens)

            # Konsumsi ')'
            if tokens and tokens[0] == ')':
                tokens.popleft()

            return {'val': operator, 'left': left, 'right': right}

        else:
            # Token adalah operand (bilangan)
            try:
                return {'val': float(token), 'left': None, 'right': None}
            except ValueError:
                raise ValueError(f"Token tidak valid: '{token}'")

    def _eval_tree(self, node: Optional[dict]) -> float:
        """
        Evaluasi pohon ekspresi secara postorder (rekursif).
        Mengembalikan nilai numerik hasil evaluasi subtree.
        """
        if node is None:
            raise ValueError("Node kosong ditemukan saat evaluasi")

        # Leaf node: operand
        if node['left'] is None and node['right'] is None:
            return node['val']

        left_val = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])
        op = node['val']

        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError("Division by zero terdeteksi dalam ekspresi")
            return left_val / right_val
        else:
            raise ValueError(f"Operator tidak dikenali: '{op}'")

    # =========================================================
    # 2. IN-PLACE MAX-HEAP CONSTRUCTION + HEAPSORT
    # =========================================================

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """Mengurutkan array secara ascending menggunakan in-place heapsort."""
        n = len(arr)
        if n <= 1:
            return arr

        # Fase 1: Bangun max-heap dari daun ke atas (bottom-up)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # Fase 2: Ekstraksi berulang — swap root (max) ke akhir, sift-down
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """
        Memulihkan heap order property dengan mendorong node ke bawah.
        Menggunakan rumus: left = 2*idx+1, right = 2*idx+2.
        """
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < heap_size and arr[left] > arr[largest]:
                largest = left
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            if largest == idx:
                break  # Heap order terpenuhi, berhenti

            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest

    # =========================================================
    # 3. COMPLETE BINARY TREE VALIDATOR
    # =========================================================

    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Memvalidasi apakah array memenuhi properti complete binary tree.
        Pada complete binary tree, semua level terisi penuh kecuali level
        terakhir yang terisi dari kiri ke kanan tanpa 'lubang'.
        Dengan pemetaan array: untuk setiap node i, left = 2i+1, right = 2i+2.
        Jika indeks child melebihi n-1 sebelum semua node internal habis,
        maka bukan complete binary tree.
        """
        n = len(arr)
        if n <= 1:
            return True

        found_none = False
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n:
                if found_none:
                    return False  # Ada "lubang" sebelum node ini
            else:
                found_none = True  # Node kiri tidak ada

            if right < n:
                if found_none:
                    return False
            else:
                found_none = True  # Node kanan tidak ada

        return True


# =========================================================
# TEST CASES
# =========================================================

if __name__ == "__main__":
    print("=" * 50)
    print("EXPRESSION TREE + EVALUASI")
    print("=" * 50)

    expr1 = "((8*5)+(9/(7-4)))"
    sorter1 = ExprHeapSorter(expr1)
    try:
        val1 = sorter1.parse_and_evaluate()
        print(f"Ekspresi : {expr1}")
        print(f"Hasil    : {val1[0]}")  # Hasilnya 43.0
    except ValueError as e:
        print(f"Error: {e}")

    print()
    expr2 = "((10+5)*(2-1))"
    sorter2 = ExprHeapSorter(expr2)
    try:
        val2 = sorter2.parse_and_evaluate()
        print(f"Ekspresi : {expr2}")
        print(f"Hasil    : {val2[0]}")
    except ValueError as e:
        print(f"Error: {e}")

    print()
    expr3 = "((4/(2-2))+1)"  # Division by zero
    sorter3 = ExprHeapSorter(expr3)
    try:
        val3 = sorter3.parse_and_evaluate()
        print(f"Ekspresi : {expr3}")
        print(f"Hasil    : {val3[0]}")
    except ValueError as e:
        print(f"Ekspresi : {expr3}")
        print(f"Error    : {e}")

    print()
    print("=" * 50)
    print("HEAPSORT IN-PLACE")
    print("=" * 50)

    sorter4 = ExprHeapSorter("")
    arr1 = [43, 12, 7, 3, 19, 5, 1, 28]
    print(f"Input:  {arr1}")
    result1 = sorter4.heapsort_inplace(arr1)
    print(f"Output: {result1}")

    print()
    arr2 = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"Input (descending): {arr2}")
    result2 = sorter4.heapsort_inplace(arr2)
    print(f"Output: {result2}")

    print()
    arr3 = [5, 5, 5, 5]
    print(f"Input (duplikat): {arr3}")
    result3 = sorter4.heapsort_inplace(arr3)
    print(f"Output: {result3}")

    print()
    print("=" * 50)
    print("COMPLETE BINARY TREE VALIDATOR")
    print("=" * 50)

    sorter5 = ExprHeapSorter("")
    arr_complete = [1, 2, 3, 4, 5, 6, 7]
    print(f"Array: {arr_complete}")
    print(f"Complete tree? {sorter5.is_complete_tree(arr_complete)}")

    arr_incomplete = [1, 2, 3, None, 5]
    arr_inc2 = [1, 2, 3, 4, 5, 6]
    print(f"Array: {arr_inc2}")
    print(f"Complete tree? {sorter5.is_complete_tree(arr_inc2)}")
