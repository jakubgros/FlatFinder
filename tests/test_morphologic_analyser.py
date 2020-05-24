import unittest

from text.analysis.morphologic_analyser import MorphologicAnalyser


class MyTestCase(unittest.TestCase):


    def test_data_extension(self):
        analyser = MorphologicAnalyser.Instance()

        # data for Bonerowska flection has been extended manually
        base_form1 = analyser.get_base_form("Bonerowskiej")
        self.assertNotEqual(len(base_form1), 0)

        base_form2 = analyser.get_base_form("Bonerowska")
        self.assertNotEqual(len(base_form2), 0)

        #TODO uncomment
        #self.assertEqual(len(base_form1), len(base_form2))

        pass

    def test_reinterpret(self):
        # morfeusz doesn't recognize oś as osiedle. We force it to reinterpret oś as osiedle and do the analysis using Morfeusz library

        analyser = MorphologicAnalyser.Instance()

        base_form = analyser.get_base_form("oś")
        self.assertNotEqual(len(base_form), 0)

        self.assertEqual(analyser.get_base_form("oś"), analyser.get_base_form("osiedle"))

if __name__ == '__main__':
    unittest.main()
