# ============================================================
# Soal 1(a) - Big Integer ADT menggunakan Singly Linked List
# Setiap digit disimpan di node terpisah, urutan dari
# least-significant (kanan) ke most-significant (kiri)
# ============================================================

class _Node:
    """Node untuk singly linked list."""
    def __init__(self, digit):
        self.digit = digit   # satu digit (0-9)
        self.next = None


class BigIntegerLinkedList:
    def __init__(self, initValue="0"):
        """
        Membuat BigInteger dari string angka.
        Contoh: BigIntegerLinkedList("45839")
        """
        self._head = None
        self._negative = False
        self._build_from_string(initValue)

    # ----------------------------------------------------------
    # Helper: build linked list dari string
    # ----------------------------------------------------------
    def _build_from_string(self, s):
        s = s.strip()
        if not s:
            s = "0"

        if s[0] == '-':
            self._negative = True
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]

        s = s.lstrip('0') or '0'

        # Simpan dari least-significant -> most-significant
        # String "45839" -> node: 9 -> 3 -> 8 -> 5 -> 4
        self._head = None
        for ch in s:
            node = _Node(int(ch))
            node.next = self._head
            self._head = node

    # ----------------------------------------------------------
    # Helper: konversi linked list ke integer Python
    # ----------------------------------------------------------
    def _to_int(self):
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        value = int(''.join(reversed(digits))) if digits else 0
        return -value if self._negative else value

    # ----------------------------------------------------------
    # Helper: buat BigIntegerLinkedList dari int Python
    # ----------------------------------------------------------
    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    # ----------------------------------------------------------
    # toString()
    # ----------------------------------------------------------
    def toString(self):
        """Mengembalikan representasi string dari big integer."""
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        result = ''.join(reversed(digits)) if digits else '0'
        if self._negative and result != '0':
            result = '-' + result
        return result

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return f"BigIntegerLinkedList('{self.toString()}')"

    # ----------------------------------------------------------
    # comparable(other)
    # Mendukung operator: <, <=, >, >=, ==, !=
    # ----------------------------------------------------------
    def __eq__(self, other):
        return self._to_int() == other._to_int()

    def __ne__(self, other):
        return self._to_int() != other._to_int()

    def __lt__(self, other):
        return self._to_int() < other._to_int()

    def __le__(self, other):
        return self._to_int() <= other._to_int()

    def __gt__(self, other):
        return self._to_int() > other._to_int()

    def __ge__(self, other):
        return self._to_int() >= other._to_int()

    # ----------------------------------------------------------
    # arithmetic(rhsInt)
    # Mendukung: +, -, *, //, %, **
    # ----------------------------------------------------------
    def __add__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() + other._to_int())

    def __sub__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() - other._to_int())

    def __mul__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() * other._to_int())

    def __floordiv__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() // other._to_int())

    def __mod__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() % other._to_int())

    def __pow__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() ** other._to_int())

    # ----------------------------------------------------------
    # bitwise-ops(rhsInt)
    # Mendukung: |, &, ^, <<, >>
    # ----------------------------------------------------------
    def __or__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() | other._to_int())

    def __and__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() & other._to_int())

    def __xor__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() ^ other._to_int())

    def __lshift__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() << other._to_int())

    def __rshift__(self, other):
        return BigIntegerLinkedList._from_int(self._to_int() >> other._to_int())


# ==============================================================
# Demo / Testing
# ==============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  Soal 1(a) - Big Integer ADT - Singly Linked List")
    print("=" * 55)

    a = BigIntegerLinkedList("45839")
    b = BigIntegerLinkedList("12345")

    print(f"\na = {a}")
    print(f"b = {b}")

    print("\n--- toString ---")
    print(f"a.toString() = {a.toString()}")

    print("\n--- Comparable ---")
    print(f"a == b : {a == b}")
    print(f"a != b : {a != b}")
    print(f"a >  b : {a > b}")
    print(f"a <  b : {a < b}")
    print(f"a >= b : {a >= b}")
    print(f"a <= b : {a <= b}")

    print("\n--- Arithmetic ---")
    print(f"a + b  = {a + b}")
    print(f"a - b  = {a - b}")
    print(f"a * b  = {a * b}")
    print(f"a // b = {a // b}")
    print(f"a %  b = {a % b}")
    print(f"b ** BigIntegerLinkedList('3') = {b ** BigIntegerLinkedList('3')}")

    print("\n--- Bitwise ---")
    x = BigIntegerLinkedList("60")
    y = BigIntegerLinkedList("13")
    print(f"x = {x} , y = {y}")
    print(f"x | y  = {x | y}")
    print(f"x & y  = {x & y}")
    print(f"x ^ y  = {x ^ y}")
    print(f"x << BigIntegerLinkedList('2') = {x << BigIntegerLinkedList('2')}")
    print(f"x >> BigIntegerLinkedList('2') = {x >> BigIntegerLinkedList('2')}")
