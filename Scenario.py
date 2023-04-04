
class Scenario:
    def __init__(self, name: str, desp: str, input_options, input_templates):
        self.name = name
        self.desp = desp
        self.options = input_options
        self.templates = input_templates
        self.rules = None
        self.locations = None
    
    def __str__(self) -> str:
        return f"Scenario Name: {self.name}, Description: {self.desp}, Options: {self.options}, Templates: {self.templates}"

    def set_rule(self, rules):
        self.rules = rules

    def set_location(self, locations: list):
        self.locations = locations