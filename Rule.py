
class Rule:
    counter = 0

    def __init__(self, rule_name: str, desp: str, rule_type: str, restriction: dict, priority: int, failure_action = None) -> None:
        self.rid = Rule.counter
        Rule.counter += 1
        self.rule_name = rule_name
        self.desp = desp
        self.rule_type = rule_type
        # A restriction is a dictionary of {type: [list of values to be restricted]}
        self.restriction = restriction
        self.priority = priority
        self.failure_action = failure_action


    def __str__(self) -> str:
        return f"<rule name: {self.rule_name}\n - priority: {self.priority}\n - description: {self.desp}>"
