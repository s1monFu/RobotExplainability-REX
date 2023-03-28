import UserInput

input_options = {"verb": ["go", "walk", "run", "drive", "fly"], "subject": ["car", "truck", "bus", "plane", "bike"], "from": [
        "home", "work", "school", "store", "park"], "to": ["home", "work", "school", "store", "park"]}
input_templates = ["[verb]", "[verb] + [subject]", "[verb] + [subject] + from [somewhere] to [somewhere]"]

user_input = UserInput.UserInput(input_options,input_templates)

# interactive mode test
# input_traces = user_input.take_input('i')
# print(input_traces)

# batch mode test
input_traces = user_input.take_input('b')
print(input_traces)
