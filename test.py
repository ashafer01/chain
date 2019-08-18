import unittest

from chain import chain, args


class TestChain(unittest.TestCase):
    def test_chain(self):
        def _test_x(x):
            return x + 'x'

        def _test_y(x):
            return x + 'y'

        def _test_z(x):
            return x + 'z'

        def _test_2(a,b):
            return a+b

        def _test_3(a,b,c):
            return a+b+c

        chain_res = chain(args('w') | _test_x | _test_y | args('2'), _test_2, _test_z, args('3', '4'), _test_3)
        native_res = _test_3(_test_z(_test_2(_test_y(_test_x('w')), '2')), '3', '4')

        self.assertEqual(chain_res, native_res)

    def test_return_args(self):
        def _test_ret_args(x):
            res = args('hello', world=x)
            return res

        def _test_accept_args(hello, world=''):
            return hello + ' ' + world

        def _test_1(x):
            return '1 ' + x

        def _test_2(x):
            return x + ' 2'

        res = chain(args('test') | _test_1 | _test_2 | _test_ret_args | _test_accept_args)
        expected = 'hello 1 test 2'
        self.assertEqual(res, expected)
