import UserInput

input_options = {"verb": ["go", "walk", "run", "drive", "fly"], "subject": ["car", "truck", "bus", "plane", "bike"], "from": [
        "home", "work", "school", "store", "park"], "to": ["home", "work", "school", "store", "park"]}

user_input = UserInput.UserInput(input_options)

# interactive mode test
# input_traces = user_input.take_input('i')
# print(input_traces)

# batch mode test
input_traces = user_input.take_input('b')
print(input_traces)
