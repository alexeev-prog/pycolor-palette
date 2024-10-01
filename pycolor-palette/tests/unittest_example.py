from math import sqrt
import unittest


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


class BasicTestCase(unittest.TestCase):
    def test_square_it_up(self):
        res = square_it_up(10)
        res2 = square_it_up(2)
        self.assertEqual(res, 100)
        self.assertEqual(res2, 4)


class SquareEqSolverTestCase(unittest.TestCase):
    def test_no_root(self):
        res = square_eq_solver(10, 0, 2)
        self.assertEqual(len(res), 0)

    def test_single_root(self):
        res = square_eq_solver(10, 0, 0)
        self.assertEqual(len(res), 1)
        self.assertEqual(res, [0])

    def test_multiple_root(self):
        res = square_eq_solver(2, 5, -3)
        self.assertEqual(len(res), 2)
        self.assertEqual(res, [0.5, -3])
