import sys
import unittest

# PyHarmonyOptimizer modülünü içe aktar
sys.path.append('../')  # Üst klasöre erişim sağlar

from pyharmonyoptimizer.PyHarmonyOptimizer import Continuous, Discrete, Constant, Categorical, Minimization, Maximization
from pyharmonyoptimizer.welded_beam_design import WeldedBeamDesign

class TestContinuousSampler(unittest.TestCase):
    def test_sample_in_range(self):
        sampler = Continuous(0, 10)
        sample = sampler.sample()
        self.assertTrue(0 <= sample <= 10, "Sample is not in the expected range")

class TestDiscreteSampler(unittest.TestCase):
    def test_sample_in_values(self):
        values = [1, 2, 3]
        sampler = Discrete(values)
        sample = sampler.sample()
        self.assertIn(sample, values, "Sample is not one of the discrete values")

# Daha fazla sampler ve optimization testleri ekleyebilirsiniz.

class TestWeldedBeamDesign(unittest.TestCase):
    def test_beam_design(self):
        beam = WeldedBeamDesign(0.1, 2.0, 0.1, 0.1)
        reference, fitness, penalty = beam.fitness()
        self.assertGreaterEqual(fitness, 0, "Fitness should be non-negative")
        self.assertGreaterEqual(penalty, 0, "Penalty should be non-negative")

# Minimization ve Maximization testleri için örnekler
class TestOptimizationAlgorithms(unittest.TestCase):
    def test_minimization_algorithm(self):
        # Bu bölümde Minimization algoritmasının testleri eklenebilir
        pass

    def test_maximization_algorithm(self):
        # Bu bölümde Maximization algoritmasının testleri eklenebilir
        pass

if __name__ == '__main__':
    unittest.main()
