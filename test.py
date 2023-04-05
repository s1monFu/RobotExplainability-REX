import Scenario
import UserInput
from Synthesizer import Synthesizer

scene = Scenario.Scenario()
scene.load(1)
# print(scene)

userinput = UserInput.UserInput()
userinput.load_from_scene(scene)
userinput.get_input('i')
# print(input)

synthesizer = Synthesizer(scene)
# synthesizer.print_rules()
# synthesizer.synthesize(input)
# print(userinput.input_answers[0])
print(synthesizer.synthesize_without_rules(userinput.input_answers[0]))