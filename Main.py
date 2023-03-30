# Robot Explanbility (REX) - A tool for explaining robot actions
# run it in interactive mode with python3 Main.py i
# or run it in batch mode with python3 Main.py b filename
import UserInput
import Rules
import Synthesizer
import Scenario
import sys

# 1. Create Scenario
input_options = {"verb": ["fetch", "grab", "inform", "put", "open", "close"], "subject": ["grocery", "food", "cup", "phone", "computer"], "from": [
    "bedroom", "living room", "garage","kitchen counter", "store" ], "to": ["bedroom", "living room", "garage", "kitchen counter", "store"]}
input_templates = ["[verb]", "[verb] + [subject]",
                   "[verb] + [subject] + from [somewhere] to [somewhere]"]
scene = Scenario.Scenario(
    "home", "A simulated home scenario", input_options, input_templates)

# 2. setup rules
rules = []
rules.append(Rules.Rule("mom's rule", "do not touch the kitchen counter", "Type 1", {
                  "from":["kitchen counter"],"to": ["kitchen counter"]}))
rules.append(Rules.Rule("dad's rule", "do not play phone or computer", "Type 1", {
                  "subject": ["phone","computer"]}))
rules.append(Rules.Rule("brother's rule", "don't play computer without him", "Type 1", {
                "subject": ["computer"]}))
                  

# 3. take in user input
user_input = UserInput.UserInput(scene.options, scene.templates)

# choose input mode
input_mode = sys.argv[1]
file_name = None
if input_mode == 'b':
    file_name = sys.argv[2]
input_traces = user_input.take_input(input_mode, file_name)

# 4. run synthesizer
syn = Synthesizer.Synthesizer(scene.options, scene.templates)
actions = syn.synthesize(input_traces, rules)

# 5. provide explanation
for action in actions:
    print(f'<<<<<')
    print(f'Action trace without rules: {action[0]}')
    if action[1] != None and action[1][1] != "":
        print(f'Action trace with rules: {action[1][1]}')
        print("Explanation: ")
        for rule_cnt in action[1][0]:
            print(
                f'The original action violates rule {rule_cnt+1}, which is the {rules[rule_cnt].rule_name}')
            print(f'{rules[rule_cnt].rule_name} specifies that {rules[rule_cnt].desp}')
    else:
        print("This action meets all rules!")
    print(f'>>>>>')
