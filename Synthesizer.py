import random


class Synthesizer:
    def __init__(self, input_options: dict, input_templates: list) -> None:
        self.input_options = input_options
        self.input_templates = input_templates

    def synthesize(self, input_answers: list, rules: list) -> list:
        actions = []
        for input in input_answers:
            # an action without any rules
            action_wor = self.synthesize_without_rules(input)
            # a list of actions, each with a rule
            action_wr = self.synthesize_with_rules(input, rules)

            actions.append((action_wor, action_wr))
        return actions

    def synthesize_without_rules(self, input: dict):
        action_trace = input[1]['verb']
        if input[0] == 2 or input[0] == 3:
            action_trace += f" {input[1]['subject']}"
        if input[0] == 3:
            action_trace += f" from {input[1]['from']} to {input[1]['to']}"
        return action_trace

    def synthesize_with_rules(self, input: dict, rules: list):
        # input is a dictionary of {type: value}
        # rules is a list of rule, a restriction is a dictionary of {type: [list of values to be restricted]}
        actions_traces = []
        original_input = input[1].copy()
        violated_rules = set()
        notChanged = True
        action_trace = ""
        for rule in rules:
            restriction = rule.restriction
            conflict = False
            applicable = True

            # Identify if the input is applicable for the rule
            all = True
            for key in restriction:
                if original_input[key] != "" and original_input[key] not in restriction[key]:
                    all = False
            if all == False:
                continue

            # apply rules
            for key in restriction:
                # if key in original_input and original_input[key] != "":
                #     # the value in input conflicts with the restriction in the rules
                #     if original_input[key] in restriction[key]:
                violated_rules.add(rule.rid)
                if notChanged:
                    r = random.randint(0, len(self.input_options[key])-1)
                    # to avoid the same value as before
                    while input[1][key] == self.input_options[key][r] or self.input_options[key][r] in restriction[key]:
                        r = (r+1) % len(self.input_options[key])
                    input[1][key] = self.input_options[key][r]
                    conflict = True
                    notChanged = False
                # else:
                #     applicable = False
            if conflict:
                action_trace = self.synthesize_without_rules(input)
                # actions_traces.append(action_trace)
        return (list(violated_rules),action_trace)
        


            

    # def validate_input(self, template_index: int , input_trace: str, ):
    #     """
    #     Validates the input trace according to the expected template. Returns True if the input trace is valid, False otherwise.
    #     """
    #     # split input trace into individual words
    #     input_words = input_trace.split()

    #     # check for template 1
    #     if template_index == 1:
    #         # check that input trace has expected number of words
    #         if len(input_words) != 1:
    #             return False
    #         # check that input word is a valid option
    #         if input_words[0] not in self.input_options["verb"]:
    #             return False

    #     # check for template 2
    #     if template_index == 2:
    #         # check that input trace has expected number of words
    #         if len(input_words) != 2:
    #             return False
    #         # check that each input word is a valid option
    #         if input_words[0] not in self.input_options["verb"]:
    #             return False
    #         if input_words[1] not in self.input_options["subject"]:
    #             return False
    #     # check for template 3
    #     if template_index == 3:
    #         # check that input trace has expected number of words
    #         if len(input_words) != 6:
    #             return False
    #         # check that each input word is a valid option
    #         if input_words[0] not in self.input_options["verb"]:
    #             return False
    #         if input_words[1] not in self.input_options["subject"]:
    #             return False
    #         if input_words[2] != "from":
    #             return False
    #         if input_words[3] not in self.input_options["from"]:
    #             return False
    #         if input_words[4] != "to":
    #             return False
    #         if input_words[5] not in self.input_options["to"]:
    #             return False
    #     # input trace is valid
    #     return True
