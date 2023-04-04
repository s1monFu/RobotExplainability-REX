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
        self.locations = []
    
    def load(self, scene_num: int):
        path = os.path.join(os.path.dirname(__file__), "Scenarios",f"Scenario_{scene_num}")
        with open(os.path.join(path, "scene.json"), 'r') as f:
            data = json.load(f)
            self.name = data["name"]
            self.desp = data["desp"]
            self.options = data["options"]
            self.templates = data["templates"]
        with open(os.path.join(path, "rules.json"), 'r') as f:
            data = json.load(f)
            

    def set_rules(self, rules: list):
        self.rules = rules

    def add_rules(self, rule):
        self.rules.append(rule)

    def set_location(self, locations: list):
        self.locations = locations

    def add_location(self, location):
        self.locations.append(location)

    def __str__(self) -> str:
        return f"Scenario Name: {self.name},\n Description: {self.desp},\n Options: {self.options},\n Templates: {self.templates}\n"