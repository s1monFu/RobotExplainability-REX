
class Rule:
    def __init__(self, input_options: dict, input_templates: list) -> None:
        self.input_options = input_options
        self.input_templates = input_templates
    
    def get_input_options(self, input_type: str) -> list:
        """
        Takes a string argument representing the input type, and returns a list of valid input options.
        """
        return self.input_options[input_type]

    def get_input_template(self, template_index: int) -> str:
        """
        Takes an integer argument representing the template index, and returns the corresponding input template.
        """
        return self.input_templates[template_index]

    def apply_rule(self, trace: str) -> str:
        pass
