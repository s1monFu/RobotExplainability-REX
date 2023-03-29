# Robot Explanbility (REX) - A tool for explaining robot actions
# run it in interactive mode with python3 Main.py i
# or run it in batch mode with python3 Main.py b filename
import UserInput
import Rules
import Synthesizer
import Scenario
import sys

# 1. Create Scenario
input_options = {"verb": ["go", "grab", "inform", "put", "open", "close"], "subject": ["grocery", "food", "cup", "phone", "computer"], "from": [
    "bedroom", "living room", "school", "store", "park"], "to": ["bedroom", "living room", "school", "store", "park"]}
input_templates = ["[verb]", "[verb] + [subject]",
                   "[verb] + [subject] + from [somewhere] to [somewhere]"]
scene = Scenario.Scenario(
    "home", "A simulated home scenario", input_options, input_templates)

# 2. setup rules
rules = []
rule = Rules.Rule("mom's rule", "no food in bedroom", "Type 1", {
                  "subject": ["food"], "to": ["bedroom"]})
rules.append(rule)

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
    if action[1] != None:
        print(f'Action trace with rules: {action[1][0][1]}')
        rule_cnt = action[1][0][0]
        print(
            f'Explanation: The original action violates rule {action[1][0][0]}, which is the {rules[rule_cnt].rule_name}')
        print(f'Rule {rule_cnt} specifies that {rules[rule_cnt].desp}')
    print(f'>>>>>')
