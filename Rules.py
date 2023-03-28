
class Rule:
    def __init__(self, rule_name: str, desp: str, rule_type: str, restriction: str) -> None:
        self.rule_name = rule_name
        self.desp = desp
        self.rule_type = rule_type
        self.restriction = restriction

    def apply_rule(self, trace: str) -> str:
        pass

    def __str__(self) -> str:
        return f"Rule Name: {self.rule_name}, Description: {self.desp}, Type: {self.rule_type}, Restriction: {self.restriction}"
