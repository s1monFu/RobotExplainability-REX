import UserInput
import Rules
import Synthesizer

input_options = {"verb": ["go", "grab", "inform", "put", "open", "close"], "subject": ["grocery", "food", "cup", "phone", "bike"], "from": [
        "bedroom", "living room", "school", "store", "park"], "to": ["bedroom", "living room", "school", "store", "park"]}
input_templates = ["[verb]", "[verb] + [subject]", "[verb] + [subject] + from [somewhere] to [somewhere]"]

# rule test
rule = Rules.Rule("mom's rule", "no food in bedroom", "Type 1", {"subject": ["food"], "to": ["bedroom"]})
print(rule)
rules = [rule]

user_input = UserInput.UserInput(input_options, input_templates)

# interactive mode test
# input_traces = user_input.take_input('i')
# print("input traces")
# print(input_traces)


# batch mode test
input_traces = user_input.take_input('b')
print("input traces")
print(input_traces)

# synthesizer test
syn = Synthesizer.Synthesizer(input_options=input_options, input_templates=input_templates)
actions = syn.synthesize(input_traces,rules)
print("action traces")
print(actions)

