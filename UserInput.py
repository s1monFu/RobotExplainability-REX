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
        # input_answer is a list of dictionary of user input
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
        if mode == 'i':
            self.input_answers.append(self.get_input_i())
        # Not finished, postpone to further development
        elif mode == 'b':
            self.input_answers = self.get_input_b(file_name)
        else:
            print("Invalid input mode")
            return None

    def get_input_i(self):
        # choose input template
        print('Choose an input template:')
        str = ""
        for i in range(len(self.input_templates)):
            str += f"{i+1}. "
            for j in range(len(self.input_templates[i])):
                str += f"[{self.input_templates[i][j]}]"
                if j != len(self.input_templates[i])-1:
                    str += " + "
            str += " "
        print(str)
        template_index = int(input('Enter template number: '))
        if template_index > len(self.input_templates):
            print("Invalid template number.")
            return self.get_input_i()
        current_ans = {}
        current_ans["index"] = template_index
        for word in self.input_templates[len(self.input_templates)-1]:
            current_ans[word] = ""
        for word in self.input_templates[template_index-1]:
            if word == "verb":
                current_ans["verb"] = self.get_verb_input()
            if word == "subject":
                current_ans["subject"] = self.get_subject_input()
            if word == "from":
                from_ans = self.get_location_input("from")
                current_ans["from"] = from_ans[0]
                current_ans["from_sub"] = from_ans[1]
            if word == "to":
                to_ans = self.get_location_input("to")
                current_ans["to"] = to_ans[0]
                current_ans["to_sub"] = to_ans[1]
        return current_ans

    def get_verb_input(self):
        print('Choose a verb:')
        str = ""
        for i in range(len(self.verbs)):
            str += f"{i+1}. {self.verbs[i]} "
        print(str)
        verb_index = int(input('Enter verb number: '))
        if verb_index > len(self.verbs):
            print("Invalid verb number.")
            return self.get_verb_input()
        return self.verbs[verb_index-1]

    def get_location_input(self, location_type: str):
        print(f'Choose a {location_type} choice:')
        str = ""
        for i in range(len(self.locations)):
            str += f"{i+1}. {self.locations[i].name} "
        print(str)
        loc_index = int(input('Enter location number: '))
        if loc_index > len(self.locations):
            print("Invalid location number.")
            return self.get_location_input(location_type)
        
        # sublocation
        if len(self.locations[loc_index-1].ungrabable) == 0:
            return (self.locations[loc_index-1], None)
        
        print(f'Choose a {location_type} sub choice: ')
        str = "0. Not applicable "
        for i in range(len(self.locations[loc_index-1].ungrabable)):
            str += f"{i+1}. {self.locations[loc_index-1].ungrabable[i].name} "
        print(str)
        sub_loc_index = int(input('Enter sub-location number: '))
        if sub_loc_index > len(self.locations[loc_index-1].ungrabable):
            print("Invalid sub-location number.")
            return self.get_location_input(location_type)
        
        if sub_loc_index == 0:
            return (self.locations[loc_index-1], None)
        # returns a location and ungrabable object pair
        return (self.locations[loc_index-1], self.locations[loc_index-1].ungrabable[sub_loc_index-1])
        

    ## Right now, the object and the location does not really match
    ## a user can pick an object that's not in the from location
    ## future work: disallow user to choose from location, and automatically set from to the current location of the object
    def get_subject_input(self):
        print(f'Choose a subject:')
        str = ""
        for i in range(len(self.grabable)):
            str += f"{i+1}. {self.grabable[i].name} "
        print(str)
        obj_index = int(input('Enter subject number: '))
        if obj_index > len(self.grabable):
            print("Invalid object number.")
            return self.get_subject_input()
        return self.grabable[obj_index-1]

    def get_input_b(self, file_name: str):
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
            return self.get_input_b(file_name)