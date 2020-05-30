import unittest

from parsers.human_name_parser import HumanNameParser, HumanName


class HumanNameParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = HumanNameParser.Instance()

    def test_human_name_not_provided_fields_are_empty_lists_by_default(self):
        human_name = HumanName()
        self.assertIsInstance(human_name.first_name, list)
        self.assertEqual(len(human_name.first_name), 0)

    def test_human_name_parsing(self):
        all_test_cases = [
            ("Jan Kowalski",
             HumanName(first_name=["Jan"], last_name=["Kowalski"])),

            ("ks. Jana Kowalskiego",
             HumanName(title=["ks"], first_name=["Jana"], last_name=["Kowalskiego"])),

            ("księdza Jana Kowalskiego",
             HumanName(title=["księdza"], first_name=["Jana"], last_name=["Kowalskiego"])),

            ("ks. abp. Jana Zenona Kowalskiego-Nowaka",
             HumanName(title=["ks", "abp"], first_name=["Jana", "Zenona"], last_name=["Kowalskiego", "Nowaka"])),

            ("Kowalskiego",
             HumanName(last_name=["Kowalskiego"])),

            ("ks. Kowalskiego",
             HumanName(title=["ks"], last_name=["Kowalskiego"])),

            ("ks. Jana",
             HumanName(title=["ks"], first_name=["Jana"]))
        ]

        for name, expected_result in all_test_cases:
            with self.subTest(name=name):
                self.assertEqual(self.parser.parse(name), expected_result)

    def test_dots_after_titles_are_ignored(self):
        self.assertEqual(self.parser.parse("inż Jan Kowalski"), self.parser.parse("inż. Jan Kowalski"))

    def test_number_epithets_are_parsed_correctly(self):
        all_test_cases = [
            ("Mieszko I",
             HumanName(first_name=["Mieszko"], numerical_epithet=["I"])),

            ("I",
             HumanName(numerical_epithet=["I"])),

            ("Jan Paweł II",
             HumanName(first_name=['Jan', 'Paweł'], numerical_epithet=['II'])),

            ("ks. Karol Wojtyła I",
             HumanName(title=['ks'], first_name=['Karol'], last_name=['Wojtyła'], numerical_epithet=['I'])),

            ("ks. Karol I Wojtyła",
             HumanName(title=['ks'], first_name=['Karol'], last_name=['Wojtyła'], numerical_epithet=['I'])),
        ]

        for name, expected_result in all_test_cases:
            with self.subTest(name=name):
                self.assertEqual(self.parser.parse(name), expected_result)
