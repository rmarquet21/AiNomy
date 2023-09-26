import unittest

from server.lib.list_utils import first, extract_till


class TestListUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_first_should_return_the_first_element_that_match_the_predicate(self):
        # Assign
        # Acts
        elt = first([(0, 1), (2, 1), (2, 2), (1, 3)], lambda e: e[0] == 2)

        # Assert
        self.assertEqual((2, 1), elt)

    def test_extract_till_should_stop_extract_when_record_match_the_predicate(self):
        # Assign
        # Acts
        _list = [1, 2, 3, 4, 5, 6]
        _new_list = extract_till(_list, lambda r: r > 4)

        # Assert
        self.assertEqual([1, 2, 3, 4], _new_list)

    def test_extract_till_should_return_empty_list_when_first_record_match_the_predicate(self):
        # Assign
        # Acts
        _list = [1, 2, 3, 4, 5, 6]
        _new_list = extract_till(_list, lambda r: r > 0)

        # Assert
        self.assertEqual([], _new_list)


if __name__ == '__main__':
    unittest.main()