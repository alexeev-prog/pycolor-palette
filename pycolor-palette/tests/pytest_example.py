from math import sqrt


def square_it_up(num: float) -> float:
    """
    square num

    :param      num:  The number
    :type       num:  float

    :returns:   value
    :rtype:     float
    """
    return num**2


def square_eq_solver(a, b, c):
    """
    решение квадратных уравнений

    :param      a:    a
    :type       a:    int/float
    :param      b:    b
    :type       b:    int/float
    :param      c:    c
    :type       c:    int/float

    :returns:   roots
    :rtype:     list
    """
    result = []
    discriminant = b * b - 4 * a * c

    if discriminant == 0:
        result.append(-b / (2 * a))
    elif discriminant > 0:
        result.append((-b + sqrt(discriminant)) / (2 * a))
        result.append((-b - sqrt(discriminant)) / (2 * a))

    return result


def test_square_it_up():
    assert square_it_up(10) == 100


def test_no_root():
    assert len(square_eq_solver(10, 0, 2)) == 0


def test_single_root():
    assert len(square_eq_solver(10, 0, 0)) == 1


def test_multiple_root():
    assert square_eq_solver(2, 5, -3) == [0.5, -3]
