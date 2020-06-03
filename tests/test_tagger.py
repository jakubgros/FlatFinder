import unittest

from text.analysis.tagger import tagger


class TaggerTest(unittest.TestCase):
    def setUp(self):
        # clears the default exceptions
        tagger.reset_contain_person_first_name_exceptions({})

    def tearDown(self):
        # restores the default exceptions
        tagger.reset_contain_person_first_name_exceptions()

    def test_does_contain_person_first_name(self):
        self.assertTrue(tagger.does_contain_person_first_name("Stefana Batorego"))
        self.assertTrue(tagger.does_contain_person_first_name("ul. Stefana Batorego"))
        self.assertTrue(tagger.does_contain_person_first_name("marsz. Józefa Piłsudskiego"))

        self.assertFalse(tagger.does_contain_person_first_name("Mistrzejowice"))
        self.assertFalse(tagger.does_contain_person_first_name("Prądnik Biały"))
        self.assertFalse(tagger.does_contain_person_first_name("Do Sanktuarium Bożego Miłosierdzia"))

    def test_contain_exceptions(self):
        # it's recognized as "Maja" first name even though it's name of a month
        self.assertTrue(tagger.does_contain_person_first_name("Aleja 3 Maja"))
        self.assertTrue(tagger.does_contain_person_first_name("Mieszkanie znajduje się przy Alei 3 Maja"))

        # now it's correctly interpreted
        tagger.reset_contain_person_first_name_exceptions({"Aleja 3 Maja": False})
        self.assertFalse(tagger.does_contain_person_first_name("Aleja 3 Maja"))
        self.assertFalse(tagger.does_contain_person_first_name("Mieszkanie znajduje się przy Alei 3 Maja"))


if __name__ == "__main__":
    unittest.main()
