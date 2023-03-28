
class Synthesizer:
    def __init__(self, input_options: dict, input_templates: list) -> None:
        self.input_options = input_options
        self.input_templates = input_templates

    def synthesize(self, input_answers: list, rules: list) -> list:
        action_trace = []
        for input in input_answers:
            action_trace.append(f"{input['verb']}")
        return f"{input_answers[0]['verb']} {input_answers[0]['subject']} from {input_answers[0]['from']} to {input_answers[0]['to']}"