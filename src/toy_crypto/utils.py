from collections.abc import Generator
from typing import NewType, TypeGuard, Any
import math


def lsb_to_msb(n: int) -> Generator[int, None, None]:
    """
    Creates a generator of bits of n, starting from the least significant bit.
    """

    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    if n < 0:
        raise ValueError("n cannot be negative")
    while n > 0:
        yield n & 1
        n >>= 1


def digit_count(x: float, b: int = 10) -> int:
    """returns the nunmber of  digits (base b) in the integer part of x"""

    x = abs(x)
    result = math.floor(math.log(x, base=b) + 1)
    return result


Prob = NewType("Prob", float)
PositiveInt = NewType("PositiveInt", int)


def is_prob(val: Any) -> TypeGuard[Prob]:
    """true if val is a float, s.t. 0.0 <= va <= 1.0"""
    if not isinstance(val, float):
        return False
    return val >= 0.0 and val <= 1.0


def is_positive_int(val: Any) -> TypeGuard[PositiveInt]:
    """true if val is a float, s.t. 0.0 <= va <= 1.0"""
    if not isinstance(val, int):
        return False
    return val >= 1


def _pbirthday_exact(n: PositiveInt, d: PositiveInt) -> Prob:
    if n >= d:
        return Prob(1.0)

    v_dn = math.perm(d, n)
    v_t = pow(d, n)

    p = 1.0 - float(v_dn / v_t)
    if not is_prob(p):
        raise Exception("this should not happen")
    return p


def _pbirthday_approx(n: PositiveInt, d: PositiveInt) -> Prob:
    if n >= d:
        return Prob(1.0)

    p = 1.0 - math.exp(-(n * n) / (2 * d))
    if not is_prob(p):
        raise Exception("this should not happen")
    return p


def pbirthday(n: int, d: int = 365, mode: str = "auto") -> Prob:
    """prob of at least 1 collision among n "people" for d possible "days".

    The "exact" method still involves floating point approximations
    and may be very slow for large n.
    """

    if not is_positive_int(n):
        raise ValueError("n must be a positive integer")
    if not is_positive_int(d):
        raise ValueError("d must be a possible integer")

    EXACT_THRESHOLD = 1000

    match mode:
        case "exact":
            return _pbirthday_exact(n, d)
        case "approximate":
            return _pbirthday_approx(n, d)
        case "auto" if n < EXACT_THRESHOLD:
            return _pbirthday_exact(n, d)
        case "auto":  # n >- EXACT_THRESHOLD
            return _pbirthday_approx(n, d)
        case _:
            raise ValueError('mode must be "auto", "exact", or  "approximate"')


def qbirthday(p:float = 0.5, d: int = 365) -> int:
    """Returns number minimum number n to get a prob of p for d "days"

    Approximation only implemented for p < 0.5
    """
    if not is_prob(p) or p == 0.0:
        raise ValueError(f'p ({p}) must be a positive probability')

    if p > 0.5:
        raise NotImplementedError("Sorry, this only works for p < .5")

    n = math.sqrt(2 * d * math.log(1.0/(1.0 - p)))
    return math.ceil(n)
