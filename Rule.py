
class Rule:
    counter = 0

    def __init__(self, rule_name: str, desp: str, rule_type: str, restriction: dict) -> None:
        self.rid = Rule.counter
        Rule.counter += 1
        self.rule_name = rule_name
        self.desp = desp
        self.rule_type = rule_type
        # A restriction is a dictionary of {type: [list of values to be restricted]}
        self.restriction = restriction


    def __str__(self) -> str:
        return f"<name: {self.rule_name}, type: {self.rule_type}, restriction: {self.restriction}>"