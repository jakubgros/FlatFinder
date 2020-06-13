import unittest

from comparators.comparison_rules.comparison_rule import ComparisonRule
from comparators.comparison_rules.comparison_rule_type import ComparisonRuleType
from comparators.comparison_rules.comparison_rules_container import ComparisonRulesContainer
from comparators.morphologic_comparator import MorphologicComparator


class TestComparisonRule(unittest.TestCase):

    def test_does_apply_uses_morphologic_comparison_by_default(self):
        rule = ComparisonRule("osiedle", rule_type=ComparisonRuleType.FORCE_CASE_INSENSITIVITY)
        self.assertTrue(rule.does_apply(subject="osiedle"))
        self.assertTrue(rule.does_apply(subject="osiedlu"))

    def test_accepts_custom_comparators(self):
        rule = ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY,
                              comparator=lambda lhs, rhs: lhs == rhs)

        self.assertTrue(rule.does_apply(subject="osiedle"))
        self.assertFalse(rule.does_apply(subject="osiedlu"))

    def test_comparison_rules_container(self):
        rules = [
            ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY),
            ComparisonRule("osiedle", "mock_rule_type"),

            ComparisonRule("ulica", "other_mock_rule_type"),
        ]

        rules_container = ComparisonRulesContainer(rules)

        self.assertTrue(rules_container.does_apply(subject="osiedle", rule_type=ComparisonRuleType.FORCE_CASE_INSENSITIVITY))
        self.assertTrue(rules_container.does_apply(subject="osiedle", rule_type="mock_rule_type"))
        self.assertFalse(rules_container.does_apply(subject="osiedle", rule_type="other_mock_rule_type"))

        self.assertTrue(rules_container.does_apply(subject="ulica", rule_type="other_mock_rule_type"))
        self.assertFalse(rules_container.does_apply(subject="ulica", rule_type="mock_rule_type"))
        self.assertFalse(rules_container.does_apply(subject="ulica", rule_type=ComparisonRuleType.FORCE_CASE_INSENSITIVITY))

    def test_comparison_rule_with_morphologic_comparator(self):
        comparator = MorphologicComparator(title_case_sensitive=True)

        self.assertFalse(comparator.equals("Osiedle Kowalskiego", "osiedle Kowalskiego"))

        rules = [ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY)]
        comparator = MorphologicComparator(title_case_sensitive=True,
                                           comparison_rules=ComparisonRulesContainer(rules))

        self.assertTrue(comparator.equals("Osiedle Kowalskiego", "osiedle Kowalskiego"))


if __name__ == '__main__':
    unittest.main()