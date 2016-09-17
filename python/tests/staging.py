from unittest import TestCase
import bayesian.staging as s


class TestRound_1_staging(TestCase):
    def test_round_1_staging(self):
        preseeding = dict(zip(range(1, 9), range(8)))
        self.assertEquals(s.round_1_staging(preseeding),
                          [[1, 2], [3, 4], [5, 6], [7, 8]])
