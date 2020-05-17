import unittest

from Tagger import Tagger


class TaggerTest(unittest.TestCase):
    def test_does_contain_person_name(self):
        self.assertTrue(Tagger.Instance().does_contain_person_first_name("Stefana Batorego"))
        self.assertTrue(Tagger.Instance().does_contain_person_first_name("ul. Stefana Batorego"))
        self.assertTrue(Tagger.Instance().does_contain_person_first_name("marsz. Józefa Piłsudskiego"))

        self.assertFalse(Tagger.Instance().does_contain_person_first_name("Mistrzejowice"))
        self.assertFalse(Tagger.Instance().does_contain_person_first_name("Prądnik Biały"))
        self.assertFalse(Tagger.Instance().does_contain_person_first_name("Do Sanktuarium Bożego Miłosierdzia"))


if __name__ == "__main__":
    unittest.main()
