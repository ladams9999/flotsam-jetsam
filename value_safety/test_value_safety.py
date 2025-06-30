import unittest
import value_safety as vs


class TestSafeGet(unittest.TestCase):
    def test_safe_get_dict_existing_key(self):
        d = {'a': 1, 'b': 2}
        self.assertEqual(vs.safe_get(d, 'a'), 1)

    def test_safe_get_dict_missing_key(self):
        d = {'a': 1}
        self.assertIsNone(vs.safe_get(d, 'b'))

    def test_safe_get_dict_missing_key_with_default(self):
        d = {'a': 1}
        self.assertEqual(vs.safe_get(d, 'b', default=42), 42)

    def test_safe_get_list_valid_index(self):
        lst = [10, 20, 30]
        self.assertEqual(vs.safe_get(lst, 1), 20)

    def test_safe_get_list_invalid_index(self):
        lst = [10, 20, 30]
        self.assertIsNone(vs.safe_get(lst, 5))

    def test_safe_get_list_invalid_index_with_default(self):
        lst = [10, 20, 30]
        self.assertEqual(vs.safe_get(lst, 5, default='missing'), 'missing')

    def test_safe_get_object_without_get_or_index(self):
        class Dummy:
            pass
        dummy = Dummy()
        self.assertEqual(vs.safe_get(dummy, 'x', default='fallback'), 'fallback')

    def test_safe_get_tuple_valid_index(self):
        t = (1, 2, 3)
        self.assertEqual(vs.safe_get(t, 2), 3)

    def test_safe_get_tuple_invalid_index(self):
        t = (1, 2, 3)
        self.assertIsNone(vs.safe_get(t, 10))


class TestCoalesce(unittest.TestCase):
    def test_coalesce_first_non_none(self):
        self.assertEqual(vs.coalesce(None, None, 3, 4), 3)

    def test_coalesce_all_none(self):
        self.assertIsNone(vs.coalesce(None, None, None))

    def test_coalesce_first_value(self):
        self.assertEqual(vs.coalesce(0, 1, 2), 0)

    def test_coalesce_empty(self):
        self.assertIsNone(vs.coalesce())

    def test_coalesce_falsey_values(self):
        self.assertEqual(vs.coalesce(None, False, 1), False)
        self.assertEqual(vs.coalesce(None, '', 'fallback'), '')


class TestSafeCast(unittest.TestCase):
    def test_safe_cast_valid(self):
        self.assertEqual(vs.safe_cast("123", int), 123)

    def test_safe_cast_invalid(self):
        self.assertIsNone(vs.safe_cast("abc", int))

    def test_safe_cast_invalid_with_default(self):
        self.assertEqual(vs.safe_cast("abc", int, default=0), 0)

    def test_safe_cast_none(self):
        self.assertIsNone(vs.safe_cast(None, int))

    def test_safe_cast_float(self):
        self.assertEqual(vs.safe_cast("3.14", float), 3.14)


class TestDig(unittest.TestCase):
    def test_dig_nested_dict(self):
        data = {'a': {'b': {'c': 42}}}
        self.assertEqual(vs.dig(data, 'a', 'b', 'c'), 42)
    
    def test_dig_using_tuple(self):
        data = {'a': {'b': {'c': 42}}}
        self.assertEqual(vs.dig(*(data, 'a', 'b', 'c')), 42)

    def test_dig_missing_key(self):
        data = {'a': {'b': {}}}
        self.assertIsNone(vs.dig(data, 'a', 'b', 'c'))

    def test_dig_missing_key_with_default(self):
        data = {'a': {'b': {}}}
        self.assertEqual(vs.dig(data, 'a', 'b', 'c', default='not found'), 'not found')

    def test_dig_list_in_dict(self):
        data = {'a': [10, 20, 30]}
        self.assertEqual(vs.dig(data, 'a', 1), 20)

    def test_dig_tuple_in_dict(self):
        data = {'a': (100, 200)}
        self.assertEqual(vs.dig(data, 'a', 0), 100)

    def test_dig_non_collection(self):
        self.assertEqual(vs.dig(123, 'a', default='fail'), 'fail')

    def test_dig_empty_dict(self):
        data = {}
        self.assertIsNone(vs.dig(data, 'a'))

    def test_dig_empty_list(self):
        data = []
        self.assertIsNone(vs.dig(data, 0))

    def test_dig_empty_tuple(self):
        data = ()
        self.assertIsNone(vs.dig(data, 0))

    def test_dig_with_non_string_keys(self):
        data = {'a': {'b': {1: 'value'}}}
        self.assertEqual(vs.dig(data, 'a', 'b', 1), 'value')

    def test_dig_with_mixed_types(self):
        data = {'a': {'b': [1, 2, {'c': 3}]}}
        self.assertEqual(vs.dig(data, 'a', 'b', 2, 'c'), 3)

    def test_dig_with_invalid_key_type(self):
        data = {'a': {'b': {}}}
        self.assertIsNone(vs.dig(data, 'a', 1, 'c'))  # Invalid key type (int instead of str)

    def test_dig_with_none_collection(self):
        self.assertIsNone(vs.dig(None, 'a', 'b'))

    def test_dig_with_empty_keys(self):
        data = {'a': {'b': 42}}
        self.assertEqual(vs.dig(data), data)  # No keys provided

    def test_dig_with_default_value(self):
        data = {'a': {'b': 42}}
        self.assertEqual(vs.dig(data, 'a', 'b', default=99), 42)
        self.assertEqual(vs.dig(data, 'a', 'c', default=99), 99)

    def test_dig_with_nested_empty_collections(self):
        data = {'a': {'b': []}}
        self.assertIsNone(vs.dig(data, 'a', 'b', 0))  # Accessing an empty list

    def test_dig_with_non_string_keys_in_nested_dict(self):
        data = {'a': {'b': {1: 'value'}}}
        self.assertEqual(vs.dig(data, 'a', 'b', 1), 'value')  # Accessing with int key

    def test_dig_with_invalid_collection_type(self):
        self.assertIsNone(vs.dig(123, 'a'))  # Non-collection type

    def test_dig_with_mixed_collections(self):
        data = {'a': {'b': [1, {'c': 3}]}}
        self.assertEqual(vs.dig(data, 'a', 'b', 1, 'c'), 3)  # Mixed collection types

    def test_dig_with_empty_nested_collections(self):
        data = {'a': {'b': {}}}
        self.assertIsNone(vs.dig(data, 'a', 'b', 'c'))  # Accessing non-existent key in empty dict

    def test_dig_with_none_as_collection(self):
        self.assertIsNone(vs.dig(None, 'a', 'b'))  # None as collection

    def test_dig_with_non_iterable_collection(self):
        class NonIterable:
            pass
        self.assertIsNone(vs.dig(NonIterable(), 'a', 'b'))  # Non-iterable type

    def test_dig_with_empty_string_keys(self):
        data = {'': {'b': 42}}
        self.assertEqual(vs.dig(data, '', 'b'), 42)  # Accessing with empty string key


if __name__ == '__main__':
    unittest.main()
    