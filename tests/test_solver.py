import unittest
from function_handler import parse_function
from newton_raphson import solve_newton_raphson

class NewtonRaphsonTests(unittest.TestCase):
    def test_lecture_example(self):
        expr, derivative = parse_function("x^3 - 8*x + 5")
        rows, converged, _ = solve_newton_raphson(expr, derivative, 0, 1e-4, 100)
        self.assertTrue(converged)
        self.assertAlmostEqual(rows[-1]["x"], 0.66112, places=4)

    def test_exp_example(self):
        expr, derivative = parse_function("exp(-x)-x")
        rows, converged, _ = solve_newton_raphson(expr, derivative, 0, 1e-4, 100)
        self.assertTrue(converged)
        self.assertAlmostEqual(rows[-1]["x"], 0.567143, places=4)

    def test_reject_unknown_name(self):
        with self.assertRaises(ValueError):
            parse_function("__import__('os').system('echo unsafe')")

if __name__ == "__main__":
    unittest.main()
