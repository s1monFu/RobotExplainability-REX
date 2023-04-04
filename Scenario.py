import Location
import Object
import Rule
import os
import json


class Scenario:
    def __init__(self):
        self.name = None
        self.desp = None
        self.options = None
        self.templates = None
        self.rules = []
        self.objects = []
        self.locations = []

    def load(self, scene_num: int):
        path = os.path.join(os.path.dirname(__file__),
                            "Scenarios", f"Scenario_{scene_num}")

        # load scenario data
        with open(os.path.join(path, "scene.json"), 'r') as f:
            data = json.load(f)
            self.name = data["name"]
            self.desp = data["desp"]
            self.options = data["options"]
            self.templates = data["templates"]

        # load rules
        with open(os.path.join(path, "rules.json"), 'r') as f:
            data = json.load(f)
            for rule in data["rules"]:
                self.rules.append(Rule.Rule(
                    rule["rule_name"], rule["desp"], rule["rule_type"], rule["restriction"]))


    def __str__(self) -> str:
        return f"Scenario Name: {self.name},\n Description: {self.desp},\n Options: {self.options},\n Templates: {self.templates}\n"
