import unittest

class ExampleTest(unittest.TestCase):
    def test_a(self):
        self.assertEqual(1, 1)
        self.assertEqual([1, 2, 3], [1, 2, 3])
