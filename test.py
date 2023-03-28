import UserInput
import Rules
import Synthesizer

input_options = {"verb": ["go", "walk", "run", "drive", "fly"], "subject": ["car", "truck", "bus", "plane", "bike"], "from": [
        "home", "work", "school", "store", "park"], "to": ["home", "work", "school", "store", "park"]}
input_templates = ["[verb]", "[verb] + [subject]", "[verb] + [subject] + from [somewhere] to [somewhere]"]

# rule test
rule = Rules.Rule("mom's rule", "no food in bedroom", "restriction", "no driving")
print(rule)

user_input = UserInput.UserInput(input_options, input_templates)

# interactive mode test
input_traces = user_input.take_input('i')
print("input traces")
print(input_traces)


# batch mode test
# input_traces = user_input.take_input('b')
# print(input_traces)

# synthesizer test
syn = Synthesizer.Synthesizer(input_options=input_options, input_templates=input_templates)
action_traces = syn.synthesize(input_traces,rule)
print("action traces")
print(action_traces)

