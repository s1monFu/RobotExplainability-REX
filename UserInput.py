# File: UserInput.py
# Author: Simon Fu
# Function: Takes user input, validates it, and generate an input trace.

from Scenario import Scenario
from Location import Location


class UserInput:
    """
    Takes user input, validates it, and generates an input trace.
    input_options: A list of valid input options dictionary {type: [list of options]}.
    """

    def __init__(self):
        self.verbs = None
        self.input_templates = None
        self.grabable = []
        self.ungrabable = []
        self.locations = []
        self.input_answers = []

    def load_from_scene(self, scene: Scenario):
        self.verbs = scene.verbs
        self.input_templates = scene.templates
        for obj in scene.objects:
            if obj.type == "grabable":
                self.grabable.append(obj)
            else:
                self.ungrabable.append(obj)
        for loc in scene.locations:
            self.locations.append(loc)

    def get_input(self, mode: str, file_name: str = None):
        input_dict = {}
        if mode == 'i':
            input_dict = self.get_input_i()
        else:
            input_dict = self.get_input_b(file_name)
        for input in input_dict:
            continue
        return input_dict

    def get_input_i(self):
        # choose input template
        print('Choose an input template:')
        for i in range(len(self.input_templates)):
            print(f"{i+1}. {self.input_templates[i]}")
        template_index = int(input('Enter template number: '))
        current_ans = {"verb": "", "subject": "", "from": "",
                       "from_sub": "", "to": "", "to_sub": ""}
        if template_index >= 1:
            current_ans["verb"] = self.get_verb_input()
        if template_index >= 2:
            current_ans["subject"] = self.get_object_input()
        if template_index == 3:
            from_ans = self.get_location_input("from")
            current_ans["from"] = from_ans[0]
            current_ans["from_sub"] = from_ans[1]
            to_ans = self.get_location_input("to")
            current_ans["to"] = to_ans[0]
            current_ans["to_sub"] = to_ans[1]
        return current_ans

    def get_verb_input(self):
        print('Choose a verb:')
        for i in range(len(self.verbs)):
            print(f"{i+1}. {self.verbs[i]}")
        verb_index = int(input('Enter verb number: '))
        return self.verbs[verb_index-1]

    def get_location_input(self, location_type: str):
        print(f'Choose a {location_type} location:')
        for i in range(len(self.locations)):
            print(f"{i+1}. {self.locations[i].name}")
        loc_index = int(input('Enter location number: '))

        if len(self.locations[loc_index-1].ungrabable) > 0:
            print(f'Choose a {location_type} sub-location: ')
            for i in range(len(self.locations[loc_index-1].ungrabable)):
                print(f"{i+1}. {self.locations[loc_index-1].ungrabable[i].name}")
            sub_loc_index = int(input('Enter sub-location number: '))
            # returns a location and ungrabable object pair
            return (self.locations[loc_index-1], self.locations[loc_index-1].ungrabable[sub_loc_index-1])
        
        return (self.locations[loc_index-1], None)
        
        

    def get_object_input(self):
        print(f'Choose a grabable object:')
        for i in range(len(self.grabable)):
            print(f"{i+1}. {self.grabable[i].name}")
        obj_index = int(input('Enter object number: '))
        return self.grabable[obj_index-1]

    def get_input_b(self, file_name: str):
        pass

    def take_input(self, mode: str, file_name: str = None):
        """
        Takes a string argument representing the input mode ('i for interactive' or 'b for batch'), and returns a list of input traces.
        """
        if mode == 'i':
            # choose input template
            print('Choose an input template:')
            for i in range(len(self.input_templates)):
                print(f"{i+1}. {self.input_templates[i]}")
            template_index = int(input('Enter template number: '))
            current_ans = {"verb": "", "subject": "", "from": "", "to": ""}
            if template_index == 1:
                current_ans["verb"] = self.get_input_option(
                    'Enter a verb:', 'verb')
                # concatenate input values into single trace
                # self.input_trace = self.input_answers["verb"]
            elif template_index == 2:
                current_ans["verb"] = self.get_input_option(
                    'Enter a verb:', 'verb')
                current_ans["subject"] = self.get_input_option(
                    'Enter a subject:', 'subject')
                # concatenate input values into single trace
                # self.input_trace = f"{self.input_answers[0]['verb']} {self.input_answers[0]['subject']}"
            elif template_index == 3:
                current_ans["verb"] = self.get_input_option(
                    'Enter a verb:', 'verb')
                current_ans["subject"] = self.get_input_option(
                    'Enter a subject:', 'subject')
                current_ans["from"] = self.get_input_option(
                    'Enter a from location:', 'from')
                current_ans["to"] = self.get_input_option(
                    'Enter a to location:', 'to')
                # concatenate input values into single trace
                # self.input_trace = f"{self.input_answers[0]['verb']} {self.input_answers[0]['subject']} from {self.input_answers[0]['from']} to {self.input_answers[0]['to']}"
            else:
                print('Invalid template number!')
                return self.take_input(mode)
            self.input_answers.append((template_index, current_ans))
            # return list containing single input trace
            return self.input_answers
        elif mode == 'b':
            # prompt user for batch file name
            try:
                # open and read batch file
                input_traces = ""
                with open(file_name) as f:
                    input_traces = f.readlines()
                for t in input_traces:
                    words = t.split(",")
                    template_index = 0
                    current_trace = {"verb": "",
                                     "subject": "", "from": "", "to": ""}
                    if len(words) == 1:
                        template_index = 1
                        current_trace["verb"] = words[0].strip()
                        # template_index = 1
                    elif len(words) == 2:
                        template_index = 2
                        # template_index = 2
                        current_trace["verb"] = words[0].strip()
                        current_trace["subject"] = words[1].strip()
                    elif len(words) == 4:
                        template_index = 3
                        current_trace["verb"] = words[0].strip()
                        current_trace["subject"] = words[1].strip()
                        current_trace["from"] = words[2].strip()
                        current_trace["to"] = words[3].strip()
                    else:
                        print(f'Invalid input trace: {t}')
                        continue
                    # if self.validate_input(template_index,t.strip()):
                    #     valid_traces.append(t.strip())
                    self.input_answers.append((template_index, current_trace))
                # return list of valid input traces
                return self.input_answers
            except FileNotFoundError:
                print('File not found!')
                return self.take_input(mode)
        else:
            # invalid mode
            print('Invalid mode!')
            return self.take_input(mode)

    def get_input_option(self, prompt: str, option_type: str):
        """
        Prompts the user with the given prompt and option type, and returns the user's chosen option.
        """
        # get valid options for given option type
        valid_options = self.input_options[option_type]
        # prompt user with given prompt and valid options
        message = f"{prompt} ({', '.join(valid_options)}): "
        input_option = input(message)
        # validate input option
        if input_option not in valid_options:
            print('Invalid input!')
            return self.get_input_option(prompt, option_type)
        # return input option
        return input_option
