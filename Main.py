# Robot Explanbility (REX) - A tool for explaining robot actions
# run it in interactive mode with python3 Main.py i x, where x is the number of scenario to load
# or run it in batch mode with python3 Main.py b filename

# 1. keywords alternatives: a preferred object if the action conflicts with the rule.
#   if no alternatives: shut down
# 2. manipulate the component of rules: different attributes
# 3. may conflict with a lower priority rule, because it has to satisfy a rule with priority


from Scenario import Scenario
from UserInput import UserInput
from Synthesizer import Synthesizer
import sys
import os
# 1. load scenario
scene = Scenario()
load_num = sys.argv[2]
scene.load(load_num)
# print(scene.objects)
# for obj in scene.objects:
#     print(obj.name)

# Explain Scenario
# print(f"Scenario: {scene.name}")
# print(scene.desp)
# for loc in scene.locations:
#     print(f'{loc.name}')
#     print(f'- Grabable objects:')
#     for obj in loc.grabable:
#         print(f' - {obj.name}')
#     print(f'- Ungrabable objects: ')
#     for obj in loc.ungrabable:
#         print(f' - {obj.name}')
#     print(">>>>>")

# 2. take in user input
userinput = UserInput()
userinput.load_from_scene(scene)

# choose input mode
input_mode = sys.argv[1]
if input_mode not in ['i', 'b']:
    print("Wrong commandline argumnt")
    print("Run the program with command line argument i for interactive mode and b for batch mode")
file_name = None
if input_mode == 'b':
    file_name = sys.argv[2]
userinput.get_input(input_mode, file_name)

# 4. run synthesizer
syn = Synthesizer(scene)
output = syn.synthesize(userinput.input_answers)
# 5. provide explanation
for action_wo_rule, traces in output:
    if traces == None:
        print(
            f"\nAction Trace: {action_wo_rule}\n<<<Action does not violate any rules>>> \n")
        continue
    change_trace = traces[0]
    rules_violated = traces[1]
    str_trace = "\n<<< Action consideration trace >>> \n"
    str_trace += f"({action_wo_rule})"
    for i in range(len(rules_violated)):
        if i != len(rules_violated):
            str_trace += f"\n  || By {rules_violated[i].rule_name}, priority {rules_violated[i].priority}, {rules_violated[i].desp}\n  \/\n"
        str_trace += f"({change_trace[i]})"
    print(str_trace)

    # Detail explanation
