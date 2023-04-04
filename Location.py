class Location:
    def __init__(self, name: str, desp: str):
        self.name = name
        self.desp = desp
        self.objects = []
        self.grabable = []
        self.ungrabable = []

    def add_object(self, obj: str):
        self.objects.append(obj)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Location):
            return self.name == __o.name
        return False

    def __str__(self) -> str:
        obj_str = ""
        for obj in self.objects:
            obj_str += str(obj) + "; "
        return f"<name: {self.name}, objects: {obj_str}>"