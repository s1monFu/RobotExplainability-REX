class Location:
    def __init__(self,name:str, desp:str):
        self.name = name
        self.desp = desp
        self.objects = []
    
    def add_object(self, obj: str):
        self.objects.append(obj)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Location):
            return self.name == __o.name
        return False