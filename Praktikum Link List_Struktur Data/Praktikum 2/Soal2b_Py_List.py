# ============================================================
# Soal 2(b) - Big Integer ADT menggunakan Python List
# Modifikasi dari Soal 1(b): ditambah assignment combo operators
# +=, -=, *=, //=, %=, **=, <<=, >>=, |=, &=, ^=
# ============================================================

class BigIntegerList:
    def __init__(self, initValue="0"):
        self._digits = []
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
        self._digits = [int(ch) for ch in reversed(s)]

    def _to_int(self):
        value = int(''.join(str(d) for d in reversed(self._digits))) if self._digits else 0
        return -value if self._negative else value

    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    def _update(self, value):
        """Helper: reset state internal dari nilai int baru."""
        self._digits = []
        self._negative = False
        self._build_from_string(str(value))

    # ----------------------------------------------------------
    # toString()
    # ----------------------------------------------------------
    def toString(self):
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
    def __or__(self, other):     return self._from_int(self._to_int() |  other._to_int())
    def __and__(self, other):    return self._from_int(self._to_int() &  other._to_int())
    def __xor__(self, other):    return self._from_int(self._to_int() ^  other._to_int())
    def __lshift__(self, other): return self._from_int(self._to_int() << other._to_int())
    def __rshift__(self, other): return self._from_int(self._to_int() >> other._to_int())

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
    print("  Soal 2(b) - Big Integer + Assignment Ops - Python List")
    print("=" * 55)

    # Semua operator dari soal 1 tetap berfungsi
    a = BigIntegerList("45839")
    b = BigIntegerList("12345")
    print(f"\na = {a}  (internal: {a._digits})")
    print(f"b = {b}  (internal: {b._digits})")
    print(f"a + b = {a + b}, a > b: {a > b}")

    # Tambahan soal 2: assignment combo operators
    print("\n--- Assignment Combo Operators ---")
    c = BigIntegerList("100")
    d = BigIntegerList("25")
    print(f"c = {c}, d = {d}")

    c += d;  print(f"c += d   -> c = {c}")
    c -= d;  print(f"c -= d   -> c = {c}")
    c *= d;  print(f"c *= d   -> c = {c}")
    c //= d; print(f"c //= d  -> c = {c}")
    c %= d;  print(f"c %%= d   -> c = {c}")

    c = BigIntegerList("2")
    c **= BigIntegerList("10")
    print(f"2 **= 10 -> c = {c}")

    c = BigIntegerList("60")
    c |= BigIntegerList("13");  print(f"60 |= 13  -> c = {c}")
    c = BigIntegerList("60")
    c &= BigIntegerList("13");  print(f"60 &= 13  -> c = {c}")
    c = BigIntegerList("60")
    c ^= BigIntegerList("13");  print(f"60 ^= 13  -> c = {c}")
    c = BigIntegerList("60")
    c <<= BigIntegerList("2");  print(f"60 <<= 2  -> c = {c}")
    c = BigIntegerList("60")
    c >>= BigIntegerList("2");  print(f"60 >>= 2  -> c = {c}")
