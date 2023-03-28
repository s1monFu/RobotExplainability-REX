# File: UserInput.py
# Author: Simon Fu
# Function: Takes user input, validates it, and generate an input trace.

class UserInput:
    """
    Takes user input, validates it, and generates an input trace.
    input_options: A list of valid input options dictionary {type: [list of options]}.
    """
    def __init__(self, input_options: dict, input_templates: list):
        self.input_options = input_options
        self.input_templates = input_templates
        self.input_answers = []

    def take_input(self, mode: str):
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
                current_ans["verb"] = self.get_input_option('Enter a verb:', 'verb')
                # concatenate input values into single trace
                # self.input_trace = self.input_answers["verb"]
            elif template_index == 2:
                current_ans["verb"] = self.get_input_option('Enter a verb:', 'verb')
                current_ans["subject"] = self.get_input_option('Enter a subject:', 'subject')
                # concatenate input values into single trace
                # self.input_trace = f"{self.input_answers[0]['verb']} {self.input_answers[0]['subject']}"
            elif template_index == 3:
                current_ans["verb"] = self.get_input_option('Enter a verb:', 'verb')
                current_ans["subject"] = self.get_input_option('Enter a subject:', 'subject')
                current_ans["from"] = self.get_input_option('Enter a from location:', 'from')
                current_ans["to"] = self.get_input_option('Enter a to location:', 'to')
                # concatenate input values into single trace
                # self.input_trace = f"{self.input_answers[0]['verb']} {self.input_answers[0]['subject']} from {self.input_answers[0]['from']} to {self.input_answers[0]['to']}"
            else:
                print('Invalid template number!')
                return self.take_input(mode)
            self.input_answers.append(current_ans)
            # return list containing single input trace
            return self.input_answers
        elif mode == 'b':
            # prompt user for batch file name
            file_name = input('Enter batch file name: ')
            try:
                # open and read batch file
                input_traces = ""
                with open(file_name) as f:
                    input_traces = f.readlines()
                for t in input_traces:
                    words = t.split(" ")
                    template_index = 0
                    current_trace = {"verb": "", "subject": "", "from": "", "to": ""}
                    if len(words) == 1:
                        current_trace["verb"] = words[0].strip()
                        # template_index = 1
                    elif len(words) == 2:
                        # template_index = 2 
                        current_trace["verb"] = words[0].strip()
                        current_trace["subject"] = words[1].strip()
                    elif len(words) == 6:
                        current_trace["verb"] = words[0].strip()
                        current_trace["subject"] = words[1].strip()
                        current_trace["from"] = words[3].strip()
                        current_trace["to"] = words[5].strip()
                    else:
                        print(f'Invalid input trace: {t}')
                        continue
                    # if self.validate_input(template_index,t.strip()):
                    #     valid_traces.append(t.strip())
                    self.input_answers.append(current_trace)
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

    def validate_input(self, template_index: int , input_trace: str):
        """
        Validates the input trace according to the expected template. Returns True if the input trace is valid, False otherwise.
        """
        # split input trace into individual words
        input_words = input_trace.split()

        # check for template 1
        if template_index == 1:
            # check that input trace has expected number of words
            if len(input_words) != 1:
                return False
            # check that input word is a valid option
            if input_words[0] not in self.input_options["verb"]:
                return False

        # check for template 2
        if template_index == 2:
            # check that input trace has expected number of words
            if len(input_words) != 2:
                return False
            # check that each input word is a valid option
            if input_words[0] not in self.input_options["verb"]:
                return False
            if input_words[1] not in self.input_options["subject"]:
                return False
        # check for template 3
        if template_index == 3:
            # check that input trace has expected number of words
            if len(input_words) != 6:
                return False
            # check that each input word is a valid option
            if input_words[0] not in self.input_options["verb"]:
                return False
            if input_words[1] not in self.input_options["subject"]:
                return False
            if input_words[2] != "from":
                return False
            if input_words[3] not in self.input_options["from"]:
                return False
            if input_words[4] != "to":
                return False
            if input_words[5] not in self.input_options["to"]:
                return False
        # input trace is valid
        return True
