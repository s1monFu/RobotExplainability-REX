import Location
import Object
import Rule
import os
import json


class Scenario:
    def __init__(self):
        self.name = None
        self.desp = None
        self.verbs = None
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
            self.verbs = data["verbs"]
            self.templates = data["templates"]

        # load rules
        with open(os.path.join(path, "rules.json"), 'r') as f:
            data = json.load(f)
            for rule in data["rules"]:
                self.rules.append(Rule.Rule(
                    rule["rule_name"], rule["desp"], rule["rule_type"], rule["restriction"], rule["priority"]))

        # load locations
        with open(os.path.join(path, "locations.json"), 'r') as f:
            data = json.load(f)
            for loc in data["locations"]:
                self.locations.append(Location.Location(
                    loc["name"], loc["desp"]))

        # # load objects
        with open(os.path.join(path, "objects.json"), 'r') as f:
            data = json.load(f)
            for obj in data["objects"]:
                new_obj = None
                for loc in self.locations:
                    if loc.name == obj["location"]:
                        new_obj = Object.Object(
                            obj["id"], obj["type"], obj["name"], obj["desp"], loc, obj["alternatives"])
                        self.objects.append(new_obj)
                        loc.add_object(new_obj)
                        if obj["type"] == "grabable":
                            loc.grabable.append(new_obj)
                        else:
                            loc.ungrabable.append(new_obj)
                # If the new object does not have a corresponding location
                if new_obj == None:
                    new_obj = Object.Object(
                            obj["id"], obj["type"], obj["name"], obj["desp"], Location.Location("Not Applicable", "Not Applicable"), obj["alternatives"])
                    self.objects.append(new_obj)
                    

    def __str__(self) -> str:
        rules = ""
        for rule in self.rules:
            rules += str(rule) + "; "
        objects = ""
        for obj in self.objects:
            objects += str(obj) + "; "
        locations = ""
        for loc in self.locations:
            locations += str(loc) + "; "
        return f"Scenario Name: {self.name},\n Description: {self.desp},\n Verb Options: {self.verbs},\n Templates: {self.templates}\n " +\
            ">>>>>\n" +\
            f"Rules: {rules}\n Objects: {objects}\n Locations: {locations}\n" +\
            "<<<<<\n"
