import unittest

from comparators.comparison_rules.comparison_rule import ComparisonRule
from comparators.comparison_rules.comparison_rule_type import ComparisonRuleType
from comparators.comparison_rules.comparison_rules_container import ComparisonRulesContainer


class TestComparisonRule(unittest.TestCase):

    def test_does_apply_uses_morphologic_comparison_by_default(self):
        rule = ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY)
        self.assertTrue(rule.does_apply("osiedle"))
        self.assertTrue(rule.does_apply("osiedlu"))

    def test_accepts_custom_comparators(self):
        rule = ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY,
                              comparator=lambda lhs, rhs: lhs == rhs)

        self.assertTrue(rule.does_apply("osiedle"))
        self.assertFalse(rule.does_apply("osiedlu"))

    def test_comparison_rules_container(self):
        rules = [
            ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY),
            ComparisonRule("osiedle", "mock_rule_type"),

            ComparisonRule("ulica", "other_mock_rule_type"),
        ]

        rules_container = ComparisonRulesContainer(rules)

        self.assertTrue(rules_container.does_apply("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY))
        self.assertTrue(rules_container.does_apply("osiedle", "mock_rule_type"))
        self.assertFalse(rules_container.does_apply("osiedle", "other_mock_rule_type"))

        self.assertTrue(rules_container.does_apply("ulica", "other_mock_rule_type"))
        self.assertFalse(rules_container.does_apply("ulica", "mock_rule_type"))
        self.assertFalse(rules_container.does_apply("ulica", ComparisonRuleType.FORCE_CASE_INSENSITIVITY))


if __name__ == '__main__':
    unittest.main()
