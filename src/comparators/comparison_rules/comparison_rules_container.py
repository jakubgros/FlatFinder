from collections import defaultdict


class ComparisonRulesContainer:
    def __init__(self, rules):
        self.all_rules = defaultdict(lambda: list())

        for rule in rules:
            self.all_rules[rule.rule_type].append(rule)

    def does_apply(self, subject, rule_type):
        requested_type_rules = self.all_rules.get(rule_type, [])

        return any(rule.does_apply(subject) for rule in requested_type_rules)
