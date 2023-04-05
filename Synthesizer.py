import random
from Scenario import Scenario
from Rule import Rule


class Synthesizer:
    def __init__(self, scene: Scenario) -> None:
        self.cur_scene = scene
        self.verbs = scene.verbs
        self.input_templates = scene.templates
        self.objects = scene.objects
        self.locations = scene.locations
        # an ordered list of rules. Each element is a tuple of (priority: int, rule)
        # rules with higher priority have a higher priority index, and are at the end of the list
        self.rules_queue = scene.rules
        self.rules_queue.sort(key=lambda x: x.priority, reverse=False)

    def print_rules(self):
        for rule in self.rules_queue:
            print(rule)

    def change_rule_priority(self, rid: int, new_priority: int):
        for rule in self.rules_queue:
            if rule.rid == rid:
                rule.priority = new_priority
                break
        self.rules_queue.sort(key=lambda x: x.priority, reverse=False)

    def synthesize(self, input_answers: list) -> list:
        actions = []
        for input in input_answers:
            # an action without any rules
            action_wor = self.synthesize_without_rules(input)
            # a list of actions, each with a rule
            action_wr = self.synthesize_with_rules(input)

            actions.append((action_wor, action_wr))
        return actions

    def synthesize_without_rules(self, input: dict):
        action_trace = input['verb']
        if input["index"] >= 2:
            action_trace += f" {input['subject'].name}"
        if input["index"] == 3:
            from_str = input["from"].name
            if input["from_sub"] != None:
                from_str += f" {input['from_sub'].name}"
            to_str = input["to"].name
            if input["to_sub"] != None:
                to_str += f" {input['to_sub'].name}"
            action_trace += f" from {from_str} to {to_str}"
        return action_trace

    def synthesize_W_rules(self, input: dict):
        # start from the beginning of the rule queue. Rules at the front have lower priority
        # they are handled first because later rules will cover their change to ealier rules
        output = input.copy()
        for rule in self.rules_queue:
            # check the type of the rule
            if rule.rule_type == "positive":
                output = self.syn_w_pos_rule(output, rule)
            elif rule.rule_type == "negative":
                output = self.syn_w_neg_rule(output)

        # the output will be the same format as the input, but with correct values after the chagne of the rules
        return self.synthesize_without_rules(output)

    def syn_w_neg_rule(self, input:dict, rule: Rule):
        # check if this rule is compatible to the input
        compatible = self.check_compatibility(input,rule)
        if not compatible:
            return input
        # 2. check if the object in input is in the restriction list
        # check for each value type
        # if it is, find an alternative in the object's alternative list
        # if not, then this input is compatible with the rule
        for rest in rule.restriction:
            if rest in input:
                if input[rest] in rule.restriction[rest]:
                    # if no alternative, randomly choose one from the object list
                    if len(input[rest].alternatives) == 0:
                        return input
                    # if there is an alternative, then change the value in input
                    else:
                        input[rest] = random.choice(input[rest].alternatives)
                        return input

        pass
    
    def check_compatibility(self, input: dict, rule: Rule) -> bool:
        # 1. check if this rule is compatible to the input
        # if all types in rule are also in the input, then it's compatible
        # if not, skip this rule
        for rest in rule.restriction:
            if rest not in input:
                return False
        return True

    def syn_w_pos_rule(self, input: dict, rule: Rule):
        # 3. if a restriction has "" in one of the types, that means that if a -
        pass

    def synthesize_with_rules(self, input: dict):
        # input is a dictionary of {type: value}
        # rules is a list of rule, a restriction is a dictionary of {type: [list of values to be restricted]}
        actions_traces = []
        original_input = input[1].copy()
        violated_rules = set()
        action_trace = ""
        for rule in self.rules_queue:
            notChanged = True
            restriction = rule.restriction

            # Identify if the input is applicable for the rule
            all = True
            # print(input[1])
            allcnt = 0
            violated_keys = []
            for key in restriction:
                # if the value in input is not in the restriction list
                if original_input[key] == "":
                    all = False
                if original_input[key] != "" and original_input[key] not in restriction[key]:
                    # print("It's setting all to false")
                    # print(original_input)
                    # print(restriction)
                    allcnt += 1
                else:
                    violated_keys.append(key)
                # if the restriction has more types than the input

            if all == False or allcnt == len(restriction):
                # print("It's in all continue")
                continue

            # apply rules
            for key in violated_keys:
                violated_rules.add(rule.rid)
                if notChanged:
                    r = random.randint(0, len(self.input_options[key])-1)
                    # to avoid the same value as before
                    while input[1][key] == self.input_options[key][r] or self.input_options[key][r] in restriction[key]:
                        r = random.randint(0, len(self.input_options[key])-1)
                    input[1][key] = self.input_options[key][r]
                    notChanged = False
            action_trace = self.synthesize_without_rules(input)
        return (list(violated_rules), action_trace)

     # to fix a potential bug: a modified input might be changed to a restricted value in another rule
