# Objects in the world. Typically related to a location. 
# In a robot action, object is often a subject, or a subordinate of a location
class Object:
    def __init__(self, id:int, type:str, name:str, description:str, location, alternatives: list ):
        self.id = id
        self.type = type
        self.name = name
        self.desp = description
        self.location = location
        self.alternatives = alternatives
    
    def in_same_location(self,other_obj):
        if self.location == other_obj.location:
            return True
        return False

    def __str__(self):
        return f"<name: {self.name}, type: {self.type}, location: {self.location.name}>"

    def __eq__(self, other):
        if isinstance(other, Object):
            return self.name == other.name
        return False