import random
from Scenario import Scenario
from Rule import Rule
from Object import Object


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
            action_wr = self.synthesize_W_rules(input)

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
        violated_rules = []
        change_trace = []
        for rule in self.rules_queue:
            # check the type of the rule
            rule_compatible = None
            if rule.rule_type == "positive":
                output, rule_compatible  = self.syn_w_pos_rule(output, rule)
            elif rule.rule_type == "negative":
                output, rule_compatible = self.syn_w_neg_rule(output, rule)

            # if rule not compatible or not violated, just continue
            if not rule_compatible:
                continue
            # rule violated
            violated_rules.append(rule)
            change_trace.append(self.synthesize_without_rules(output))

        if len(violated_rules) == 0:
            return None
        # the output will be the same format as the input, but with correct values after the chagne of the rules
        return (change_trace, violated_rules)

    def syn_w_neg_rule(self, input: dict, rule: Rule):
        # check if this rule is compatible to the input
        compatible = self.neg_rule_check_compatibility(input, rule)
        if not compatible:
            return (input, False)
        rule_violated = False
        # 2. check if the object in input is in the restriction list
        ## check for each value type
        ## if it is, find an alternative in the object's alternative list
        ## if not, then this input is compatible with the rule     
        for rest in rule.restriction:
            if input[rest]!= None and input[rest]!="" and input[rest].name in rule.restriction[rest]:
                rule_violated = True
                # if the input is restricted, different policy for different types of value
                if rest == "verb":
                    input = self.replace_verb(input)
                if rest == "subject":
                    input = self.replace_subject(input)
                if rest == "to":
                    input = self.replace_to(input)
                if rest == "to_sub":
                    input = self.replace_to_sub(input)
        return (input, rule_violated)

    def replace_subject(self,input: dict):
        # if no alternatives to replace
        if len(input["subject"].alternatives) == 0:
            input["subject"] = ""
            return input
        # the first in the alternative list is the choice
        alt_idx = input["subject"].alternatives[0]
        # find the object in the overall object list
        for obj in self.objects:
            if obj.id == alt_idx:
                input["subject"] = obj
                return input

    def replace_verb(self,input: dict):
        pass

    def replace_to(self, input:dict):
        pass

    def replace_to_sub(self, input: dict) -> dict:
        # if no alternatives to replace
        if len(input["to_sub"].alternatives) == 0:
            input["to_sub"] = ""
            return input
        # the first in the alternative list is the choice
        alt_idx = input["to_sub"].alternatives[0]
        # find the object in the overall object list
        for obj in self.objects:
            if obj.id == alt_idx:
                input["to_sub"] = obj
                return input
        
    def neg_rule_check_compatibility(self, input: dict, rule: Rule) -> bool:
        # 1. check if this rule is compatible to the input
        # if the type in the rule restriction is also in the input type, then this rule can apply to this input
        # if not, skip this rule
        compatible = False
        for rest in rule.restriction:
            if rest in input and input[rest] != None:
                compatible = True
        return compatible

    def syn_w_pos_rule(self, input: dict, rule: Rule):
        # 3. if a restriction has "" in one of the types, that means that if a -
        # compatible = self.neg_rule_check_compatibility(input, rule)
        # if not compatible:
        #     print(">>>>>returns false here")
        #     return (input, False)
        rule_violated = False
        for rest in rule.restriction:
            if input[rest]== None or input[rest] == "" :
                rule_violated = True
                if rest == "to_sub":
                    input = self.fill_to_sub(input, rule)
        return (input, rule_violated)
    
    def fill_to_sub(self,input: dict, rule: Rule):
        name = rule.restriction["to_sub"][0]
        for obj in self.objects:
            if obj.name == name:
                input["to_sub"] = obj
        return input
