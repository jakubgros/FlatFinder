from collections import defaultdict


class ExceptionRulesContainer:
    def __init__(self, rules_list):
        self.rules_dict = defaultdict(lambda: list())
        for rule in rules_list:
            self.rules_dict[rule.rule_type].append(rule)

    @classmethod
    def empty(cls):
        return cls([])

    def does_apply(self, subject, rule_type):
        rules_for_the_type = self.rules_dict[rule_type]

        return any(rule.does_apply(subject) for rule in rules_for_the_type)
