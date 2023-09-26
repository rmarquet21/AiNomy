"""
this file is here to allow test runner of pycharm to
recognize the directory units as root for unit testing
"""

import unittest


class TestEmpty(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
