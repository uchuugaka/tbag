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


if __name__ == '__main__':
    unittest.main()
