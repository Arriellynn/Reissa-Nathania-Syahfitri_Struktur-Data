# ============================================================
# Soal 1(b) - Big Integer ADT menggunakan Python List
# Digit disimpan dalam list, indeks 0 = least-significant
# ============================================================

class BigIntegerList:
    def __init__(self, initValue="0"):
        """
        Membuat BigInteger dari string angka.
        Contoh: BigIntegerList("45839")
        """
        self._digits = []
        self._negative = False
        self._build_from_string(initValue)

    # ----------------------------------------------------------
    # Helper: build dari string
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

        # "45839" -> [9, 3, 8, 5, 4]  (index 0 = least significant)
        self._digits = [int(ch) for ch in reversed(s)]

    # ----------------------------------------------------------
    # Helper: konversi ke int Python
    # ----------------------------------------------------------
    def _to_int(self):
        value = int(''.join(str(d) for d in reversed(self._digits))) if self._digits else 0
        return -value if self._negative else value

    # ----------------------------------------------------------
    # Helper: buat BigIntegerList dari int Python
    # ----------------------------------------------------------
    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    # ----------------------------------------------------------
    # toString()
    # ----------------------------------------------------------
    def toString(self):
        """Mengembalikan representasi string dari big integer."""
        if not self._digits:
            return "0"
        result = ''.join(str(d) for d in reversed(self._digits))
        if self._negative and result != '0':
            result = '-' + result
        return result

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return f"BigIntegerList('{self.toString()}')"

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
        return BigIntegerList._from_int(self._to_int() + other._to_int())

    def __sub__(self, other):
        return BigIntegerList._from_int(self._to_int() - other._to_int())

    def __mul__(self, other):
        return BigIntegerList._from_int(self._to_int() * other._to_int())

    def __floordiv__(self, other):
        return BigIntegerList._from_int(self._to_int() // other._to_int())

    def __mod__(self, other):
        return BigIntegerList._from_int(self._to_int() % other._to_int())

    def __pow__(self, other):
        return BigIntegerList._from_int(self._to_int() ** other._to_int())

    # ----------------------------------------------------------
    # bitwise-ops(rhsInt)
    # Mendukung: |, &, ^, <<, >>
    # ----------------------------------------------------------
    def __or__(self, other):
        return BigIntegerList._from_int(self._to_int() | other._to_int())

    def __and__(self, other):
        return BigIntegerList._from_int(self._to_int() & other._to_int())

    def __xor__(self, other):
        return BigIntegerList._from_int(self._to_int() ^ other._to_int())

    def __lshift__(self, other):
        return BigIntegerList._from_int(self._to_int() << other._to_int())

    def __rshift__(self, other):
        return BigIntegerList._from_int(self._to_int() >> other._to_int())


# ==============================================================
# Demo / Testing
# ==============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  Soal 1(b) - Big Integer ADT - Python List")
    print("=" * 55)

    a = BigIntegerList("45839")
    b = BigIntegerList("12345")

    print(f"\na = {a}  (internal digits: {a._digits})")
    print(f"b = {b}  (internal digits: {b._digits})")

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
    print(f"b ** BigIntegerList('3') = {b ** BigIntegerList('3')}")

    print("\n--- Bitwise ---")
    x = BigIntegerList("60")
    y = BigIntegerList("13")
    print(f"x = {x} , y = {y}")
    print(f"x | y  = {x | y}")
    print(f"x & y  = {x & y}")
    print(f"x ^ y  = {x ^ y}")
    print(f"x << BigIntegerList('2') = {x << BigIntegerList('2')}")
    print(f"x >> BigIntegerList('2') = {x >> BigIntegerList('2')}")
