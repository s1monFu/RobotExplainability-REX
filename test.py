import Scenario
import UserInput

scene = Scenario.Scenario()
scene.load(1)
print(scene)

userinput = UserInput.UserInput()
userinput.load_from_scene(scene)
input = userinput.get_input('i')
print(input)
