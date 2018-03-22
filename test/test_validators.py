# -*- coding:utf-8 -*-

import unittest

from tbag.core import exceptions
from tbag.utils import validators


class TestValidators(unittest.TestCase):

    def test_bool_field(self):
        # check True
        fields = [True, "True", "true"]
        for field in fields:
            with self.subTest(field):
                self.assertEqual(validators.bool_field(field), True)
        datas = [{'a': True}, {'a': "True"}, {'a': "true"}]
        for data in datas:
            with self.subTest(data):
                self.assertEqual(validators.bool_field(data, 'a'), True)

        # check False
        fields = [False, "False", "false"]
        for field in fields:
            with self.subTest(field):
                self.assertEqual(validators.bool_field(field), False)
        datas = [{'a': False}, {'a': "False"}, {'a': "false"}]
        for data in datas:
            with self.subTest(data):
                self.assertEqual(validators.bool_field(data, 'a'), False)

        # check not required
        data = {'a': True}
        self.assertEqual(validators.bool_field(data, 'b', False), None)

        # check raise error
        with self.assertRaises(exceptions.ValidationError):
            self.assertEqual(validators.bool_field(None), True)
            self.assertEqual(validators.bool_field("a"), True)
            self.assertEqual(validators.bool_field(None, 'a'), True)
        with self.assertRaises(exceptions.SystemError):
            self.assertEqual(validators.bool_field("bc", 'a'), True)

    def test_int_field(self):
        # check int
        fields = [111, "111", 111.11, "111"]
        for field in fields:
            with self.subTest(field):
                self.assertEqual(validators.int_field(field), 111)
        datas = [{'a': 111}, {'a': "111"}, {'a': 111.11}, {'a': "111"}]
        for data in datas:
            with self.subTest(data):
                self.assertEqual(validators.int_field(data, 'a'), 111)

        # check not required
        data = {'a': True}
        self.assertEqual(validators.int_field(data, 'b', False), None)

        # check raise error
        with self.assertRaises(exceptions.ValidationError):
            self.assertEqual(validators.int_field(None), 11)
            self.assertEqual(validators.int_field("a"), 1)
            self.assertEqual(validators.int_field(None, 'a'), 1)
        with self.assertRaises(exceptions.SystemError):
            self.assertEqual(validators.int_field("bc", 'a'), 1)


if __name__ == '__main__':
    unittest.main()
