from scripts.helpers.utils import countdown, normalize

import unittest
import time
import random


class TestUtils(unittest.TestCase):
    def test_countdown(self):
        it = time.time()
        s = int(random.random() * 5)
        while not countdown(it, s):
            pass

        self.assertTrue(time.time() - it > s)

    def test_normalize(self):
        l = 0
        t = 100

        for i in range(l, t):
            self.assertEqual(normalize(i, l, t), (i / t))
