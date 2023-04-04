# Objects in the world. Typically related to a location. 
# In a robot action, object is often a subject, or a subordinate of a location
class Object:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.location = None
        self.alternatives = {}

    def set_location(self, location):
        self.location = location

    def add_alternative(self, priority: int, alternative):
        if self.alternatives[priority] == None:
            self.alternatives[priority] = []
        self.alternatives[priority].append(alternative)

    def get_alternative(self, restriction: list):
        for key, obj in self.alternatives:
            if obj not in restriction:
                return obj
    
    def in_same_location(self,other_obj):
        if self.location == other_obj.location:
            return True
        return False

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Object):
            return self.name == other.name
        return False