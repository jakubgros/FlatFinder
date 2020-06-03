import unittest

from text.analysis.morphologic_analyser import morphologic_analyser


class TestMorphologicAnalyser(unittest.TestCase):
    def setUp(self):
        # clears the default base form extension and reinterpret mapping
        morphologic_analyser.reset_base_form_extension({})
        morphologic_analyser.reset_reinterpret_mapping({})
        morphologic_analyser.reset_base_form_removals({})

    def tearDown(self):
        # restores the default base form extension and reinterpret mapping
        morphologic_analyser.reset_base_form_extension()
        morphologic_analyser.reset_reinterpret_mapping()
        morphologic_analyser.reset_base_form_removals()

    def test_get_base_form(self):
        analyser = morphologic_analyser
        self.assertEqual(analyser.get_base_form("profesora"), {"profesor"})

    def test_base_form_extension(self):
        analyser = morphologic_analyser

        base_form = analyser.get_base_form("profesora")
        self.assertNotIn("manually added base form", base_form)

        base_form = analyser.get_base_form("profesorem")
        self.assertNotIn("manually added base form", base_form)

        base_form = analyser.get_base_form("profesorowi")
        self.assertNotIn("manually added base form", base_form)

        analyser.reset_base_form_extension({"manually added base form": ("profesora", "profesorem")})

        base_form = analyser.get_base_form("profesora")
        self.assertIn("manually added base form", base_form)

        base_form = analyser.get_base_form("profesorem")
        self.assertIn("manually added base form", base_form)

        base_form = analyser.get_base_form("profesorowi")
        self.assertNotIn("manually added base form", base_form)

    def test_base_form_removals(self):
        analyser = morphologic_analyser
        base_form = analyser.get_base_form("Kraków")
        self.assertIn("Krak", base_form)

        analyser.reset_base_form_removals({"Kraków": ("Krak",)})

        base_form = analyser.get_base_form("Kraków")
        self.assertNotIn("Krak", base_form)

    def test_reinterpret(self):
        """ The class doesn't recognize some words correctly. For example initially it didn't recognize 'oś' as
        'osiedle'. We can force it to reinterpret 'oś' as 'osiedle' and do the analysis against
        the 'osiedle' word - we do it by default in constructor, but for testing purposes we cleared
        the reinterpret mapping in setUp method """

        analyser = morphologic_analyser

        base_form = analyser.get_base_form("oś")
        self.assertNotEqual(len(base_form), 0)

        analyser.reset_reinterpret_mapping({"osiedle": ("oś", "os")})
        base_form1 = analyser.get_base_form("oś")
        base_form2 = analyser.get_base_form("os")
        base_form3 = analyser.get_base_form("osiedle")
        self.assertTrue(base_form1 == base_form2 == base_form3)


if __name__ == '__main__':
    unittest.main()
