class AnyInstance:
    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, other):
        return type(other) == self.cls
