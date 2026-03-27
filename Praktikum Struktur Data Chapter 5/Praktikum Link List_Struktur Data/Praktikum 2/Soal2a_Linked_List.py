# ============================================================
# Soal 2(a) - Big Integer ADT menggunakan Singly Linked List
# Modifikasi dari Soal 1(a): ditambah assignment combo operators
# +=, -=, *=, //=, %=, **=, <<=, >>=, |=, &=, ^=
# ============================================================

class _Node:
    """Node untuk singly linked list."""
    def __init__(self, digit):
        self.digit = digit
        self.next = None


class BigIntegerLinkedList:
    def __init__(self, initValue="0"):
        self._head = None
        self._negative = False
        self._build_from_string(initValue)

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
        self._head = None
        for ch in s:
            node = _Node(int(ch))
            node.next = self._head
            self._head = node

    def _to_int(self):
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        value = int(''.join(reversed(digits))) if digits else 0
        return -value if self._negative else value

    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    def _update(self, value):
        """Helper: reset state internal dari nilai int baru."""
        self._head = None
        self._negative = False
        self._build_from_string(str(value))

    # ----------------------------------------------------------
    # toString()
    # ----------------------------------------------------------
    def toString(self):
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
    # ----------------------------------------------------------
    def __eq__(self, other): return self._to_int() == other._to_int()
    def __ne__(self, other): return self._to_int() != other._to_int()
    def __lt__(self, other): return self._to_int() <  other._to_int()
    def __le__(self, other): return self._to_int() <= other._to_int()
    def __gt__(self, other): return self._to_int() >  other._to_int()
    def __ge__(self, other): return self._to_int() >= other._to_int()

    # ----------------------------------------------------------
    # arithmetic(rhsInt)
    # ----------------------------------------------------------
    def __add__(self, other):      return self._from_int(self._to_int() +  other._to_int())
    def __sub__(self, other):      return self._from_int(self._to_int() -  other._to_int())
    def __mul__(self, other):      return self._from_int(self._to_int() *  other._to_int())
    def __floordiv__(self, other): return self._from_int(self._to_int() // other._to_int())
    def __mod__(self, other):      return self._from_int(self._to_int() %  other._to_int())
    def __pow__(self, other):      return self._from_int(self._to_int() ** other._to_int())

    # ----------------------------------------------------------
    # bitwise-ops(rhsInt)
    # ----------------------------------------------------------
    def __or__(self, other):      return self._from_int(self._to_int() |  other._to_int())
    def __and__(self, other):     return self._from_int(self._to_int() &  other._to_int())
    def __xor__(self, other):     return self._from_int(self._to_int() ^  other._to_int())
    def __lshift__(self, other):  return self._from_int(self._to_int() << other._to_int())
    def __rshift__(self, other):  return self._from_int(self._to_int() >> other._to_int())

    # ----------------------------------------------------------
    # Assignment combo operators (TAMBAHAN SOAL 2)
    # ----------------------------------------------------------
    def __iadd__(self, other):      self._update(self._to_int() +  other._to_int()); return self
    def __isub__(self, other):      self._update(self._to_int() -  other._to_int()); return self
    def __imul__(self, other):      self._update(self._to_int() *  other._to_int()); return self
    def __ifloordiv__(self, other): self._update(self._to_int() // other._to_int()); return self
    def __imod__(self, other):      self._update(self._to_int() %  other._to_int()); return self
    def __ipow__(self, other):      self._update(self._to_int() ** other._to_int()); return self
    def __ilshift__(self, other):   self._update(self._to_int() << other._to_int()); return self
    def __irshift__(self, other):   self._update(self._to_int() >> other._to_int()); return self
    def __ior__(self, other):       self._update(self._to_int() |  other._to_int()); return self
    def __iand__(self, other):      self._update(self._to_int() &  other._to_int()); return self
    def __ixor__(self, other):      self._update(self._to_int() ^  other._to_int()); return self


# ==============================================================
# Demo / Testing
# ==============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  Soal 2(a) - Big Integer + Assignment Ops - Linked List")
    print("=" * 55)

    # Semua operator dari soal 1 tetap berfungsi
    a = BigIntegerLinkedList("45839")
    b = BigIntegerLinkedList("12345")
    print(f"\na = {a}, b = {b}")
    print(f"a + b = {a + b}, a > b: {a > b}")

    # Tambahan soal 2: assignment combo operators
    print("\n--- Assignment Combo Operators ---")
    c = BigIntegerLinkedList("100")
    d = BigIntegerLinkedList("25")
    print(f"c = {c}, d = {d}")

    c += d;  print(f"c += d   -> c = {c}")
    c -= d;  print(f"c -= d   -> c = {c}")
    c *= d;  print(f"c *= d   -> c = {c}")
    c //= d; print(f"c //= d  -> c = {c}")
    c %= d;  print(f"c %%= d   -> c = {c}")

    c = BigIntegerLinkedList("2")
    c **= BigIntegerLinkedList("10")
    print(f"2 **= 10 -> c = {c}")

    c = BigIntegerLinkedList("60")
    c |= BigIntegerLinkedList("13");  print(f"60 |= 13  -> c = {c}")
    c = BigIntegerLinkedList("60")
    c &= BigIntegerLinkedList("13");  print(f"60 &= 13  -> c = {c}")
    c = BigIntegerLinkedList("60")
    c ^= BigIntegerLinkedList("13");  print(f"60 ^= 13  -> c = {c}")
    c = BigIntegerLinkedList("60")
    c <<= BigIntegerLinkedList("2");  print(f"60 <<= 2  -> c = {c}")
    c = BigIntegerLinkedList("60")
    c >>= BigIntegerLinkedList("2");  print(f"60 >>= 2  -> c = {c}")
