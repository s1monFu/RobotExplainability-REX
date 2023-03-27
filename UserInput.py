# File: UserInput.py
# Author: Simon Fu
# Function: Takes user input, validates it, and generate an input trace.

class UserInput:
    def __init__(self, input_options):
        self.input_options = input_options

    def take_input(self, mode):
        """
        Takes a string argument representing the input mode ('i for interactive' or 'b for batch'), and returns a list of input traces.
        """
        if mode == 'i':
            # prompt user for input
            input_verb = self.get_input_option('Enter a verb:', 'verb')
            input_subject = self.get_input_option('Enter a subject:', 'subject')
            input_from = self.get_input_option('Enter a from location:', 'from')
            input_to = self.get_input_option('Enter a to location:', 'to')
            # concatenate input values into single trace
            input_trace = f"{input_verb} {input_subject} from {input_from} to {input_to}"
            # return list containing single input trace
            return [input_trace]
        elif mode == 'b':
            # prompt user for batch file name
            file_name = input('Enter batch file name: ')
            try:
                # open and read batch file
                with open(file_name) as f:
                    input_traces = f.readlines()
                # strip whitespace and filter out invalid input traces
                input_traces = [t.strip() for t in input_traces if self.validate_input(t.strip())]
                # return list of valid input traces
                return input_traces
            except FileNotFoundError:
                print('File not found!')
                return self.take_input(mode)
        else:
            # invalid mode
            print('Invalid mode!')
            return self.take_input(mode)

    def get_input_option(self, prompt, option_type):
        """
        Prompts the user with the given prompt and option type, and returns the user's chosen option.
        """
        # get valid options for given option type
        valid_options = [o for o in self.input_options if o.startswith(option_type)]
        # prompt user with given prompt and valid options
        message = f"{prompt} ({', '.join(valid_options)}): "
        input_option = input(message)
        # validate input option
        if input_option not in valid_options:
            print('Invalid input!')
            return self.get_input_option(prompt, option_type)
        # return input option
        return input_option

    def validate_input(self, input_trace):
        """
        Validates the input trace according to the expected template. Returns True if the input trace is valid, False otherwise.
        """
        # split input trace into individual words
        input_words = input_trace.split()
        # check that input trace has expected number of words
        if len(input_words) != 5:
            return False
        # check that each input word is a valid option
        for i in range(len(input_words)):
            if input_words[i] not in self.input_options:
                return False
            # check that certain word pairs have expected structure
            if i == 1 and not input_words[i].startswith('subject'):
                return False
            if i == 3 and input_words[i] != 'from':
                return False
        # input trace is valid
        return True
