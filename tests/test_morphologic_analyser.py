import unittest

from text.analysis.morphologic_analyser import MorphologicAnalyser


class TestMorphologicAnalyser(unittest.TestCase):

    def test_get_base_form(self):
        analyser = MorphologicAnalyser.Instance()
        self.assertEqual(analyser.get_base_form("profesora"), {"profesor"})

    def test_base_form_extension(self):
        analyser = MorphologicAnalyser.Instance()
        analyser.reset_base_form_extension({"manually added base form": ("profesora", "profesorem")})

        base_form = analyser.get_base_form("profesora")
        self.assertTrue(base_form == {"profesor", "manually added base form"})

        base_form = analyser.get_base_form("profesorem")
        self.assertTrue(base_form == {"profesor", "manually added base form"})

        base_form = analyser.get_base_form("profesorowi")
        self.assertTrue(base_form == {"profesor"})

    def test_reinterpret(self):
        # The class doesn't recognize some words correctly. For example it doesn't recognize 'oś' as 'osiedle'.
        # We can force it to reinterpret 'oś' as 'osiedle' and do the analysis against the 'osiedle' word

        analyser = MorphologicAnalyser.Instance()

        analyser.reset_reinterpret_mapping()  # clear default mapping
        base_form = analyser.get_base_form("oś")
        self.assertNotEqual(len(base_form), 0)

        analyser.reset_reinterpret_mapping({"osiedle": ("oś", "os")})
        base_form1 = analyser.get_base_form("oś")
        base_form2 = analyser.get_base_form("os")
        base_form3 = analyser.get_base_form("osiedle")
        self.assertTrue(base_form1 == base_form2 == base_form3)


if __name__ == '__main__':
    unittest.main()
