from collections import defaultdict


class ComparisonRulesContainer:
    def __init__(self, rules):
        self.all_rules = defaultdict(list)

        for rule in rules:
            self.all_rules[rule.rule_type].append(rule)

    def does_apply(self, subject, rule_type):
        requested_type_rules = self.all_rules.get(rule_type, [])

        return any(rule.does_apply(subject) for rule in requested_type_rules)

    def get_filtered(self, filter):
        as_list = [rule for rules_of_particular_type in self.all_rules.values() for rule in rules_of_particular_type]
        filtered = [rule for rule in as_list if filter(rule)]
        filtered_container = ComparisonRulesContainer(filtered)
        return filtered_container