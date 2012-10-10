from django.test import TestCase

from cacheutils.decorators import cached


class TestCached(TestCase):
    def setUp(self):
        # the list instance is shared between calls
        def my_function(_list=[0]):
            _list[0] += 1
            return _list[0]

        self.my_function = my_function

    def test_my_function(self):
        self.assertEqual(self.my_function(), 1)
        self.assertEqual(self.my_function(), 2)

    def test_simple_cached_function(self):
        cached_function = cached()(self.my_function)
        self.assertEqual(cached_function(), 1)
        self.assertEqual(cached_function(), 1)
