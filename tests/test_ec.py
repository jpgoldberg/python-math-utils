import pytest
from math_utils.ec import Curve, Point, Modulus


"""
Test point arithmetic on curve over Finite Fields
"""

# Curve from Serious Cryptography
sc_parameters = (-4, 0, Modulus(191))
sc_generator = (146, 131)
curve = Curve(*sc_parameters)
Px = 3
Py = 46
Qx = 146


def test_curve_repr() -> None:
    expected = "y^2 = x^3 - 4x + 0 (mod 191)"
    name = f"{curve}"
    assert name == expected


def test_PQ_setup() -> None:
    P = Point(Px, Py, curve)
    exp_P = 3, 46

    assert P.x == exp_P[0]
    assert P.y == exp_P[1]


def test_sums_on_curve() -> None:
    c = curve

    y = c.compute_y(Px)
    if not y:
        pytest.fail("failed to compute Py")
    else:
        Py = y[0]

    y = c.compute_y(Qx)
    if not y:
        pytest.fail("failed to compute Qy")
    else:
        Qy = y[0]

    P = Point(Px, Py, c)
    Q = Point(Qx, Qy, c)

    PpQ = P.add(Q)
    assert PpQ.on_curve()

    P2 = P.double()
    assert P2.on_curve()


def test_generation():
    c = curve

    G = Point(*(sc_generator), c)
    for d in range(3, 28):
        dG = G.scaler_multiply(d)
        assert dG.on_curve()

    PaI = c.PAI
    order = (c.p + 1) // 2
    oG = G.scaler_multiply(order)
    assert oG == PaI  # f'order ({order} G = {oG}'
    assert G == G.scaler_multiply(1)
    G1 = G.scaler_multiply(order + 1)
    assert G1 == G


def test_pai() -> None:
    c = curve
    PaI = c.PAI
    P = Point(Px, Py, c)
    negP = -P

    assert PaI.is_zero
    assert PaI + P == P
    assert P + PaI == P
    assert P - P == PaI
    assert negP + P == PaI


def test_validation() -> None:
    with pytest.raises(ValueError):
        Curve(2, 3, p=Modulus(31 * 73))

    with pytest.raises(ValueError):
        Curve(2, 3, p=Modulus(5))

    with pytest.raises(ValueError):
        Point(Px, Py + 1, curve)
