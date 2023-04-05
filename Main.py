# Robot Explanbility (REX) - A tool for explaining robot actions
# run it in interactive mode with python3 Main.py i
# or run it in batch mode with python3 Main.py b filename

# 1. keywords alternatives: a preferred object if the action conflicts with the rule.
#   if no alternatives: shut down
# 2. manipulate the component of rules: different attributes
# 3. may conflict with a lower priority rule, because it has to satisfy a rule with priority


import UserInput
import Rule
import Synthesizer
import Scenario
import sys
import os

# 1. load scenario
scene = Scenario.Scenario()
scene.load(1)

# 2. take in user input
user_input = UserInput.UserInput(scene.options, scene.templates)

## choose input mode
input_mode = sys.argv[1]
file_name = None
if input_mode == 'b':
    file_name = sys.argv[2]
input_traces = user_input.get_input(input_mode, file_name)

# 4. run synthesizer
syn = Synthesizer.Synthesizer(scene.options, scene.templates)
rules = scene.rules
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
