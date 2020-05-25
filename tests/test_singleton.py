import unittest

from decorators.singleton import Singleton


class TestSingleton(unittest.TestCase):

    def test_instance_creation_is_possible_only_using_special_method(self):

        @Singleton
        class SampleClass:
            pass

        with self.assertRaises(TypeError) as context:
            SampleClass()

        self.assertTrue('Singletons must be accessed through `Instance()`.' in str(context.exception))

        inst = SampleClass.Instance()
        self.assertIsNotNone(inst)

    def test_singleton_returns_the_same_instance_each_time(self):

        @Singleton
        class SampleClass:
            pass

        inst = SampleClass.Instance()
        self.assertIsNotNone(inst)
        inst2 = SampleClass.Instance()
        self.assertIs(inst, inst2)

    def test_class_is_not_interpreted_as_wrapper(self):

        @Singleton
        class SampleClass:
            """SampleClass documentation"""

        inst = SampleClass.Instance()
        self.assertEqual(inst.__doc__, 'SampleClass documentation')


if __name__ == '__main__':
    unittest.main()
