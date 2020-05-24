from collections import defaultdict


class ComparisonRulesContainer:
    def __init__(self, rules_list):
        self.rules_dict = defaultdict(lambda: list())
        for rule in rules_list:
            self.rules_dict[rule.rule_type].append(rule)

    def does_apply(self, subject, rule_type):
        if rule_type not in self.rules_dict:
            return False

        rules_for_the_type = self.rules_dict[rule_type]

        return any(rule.does_apply(subject) for rule in rules_for_the_type)
