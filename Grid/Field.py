class field:
    def __init__(self, x, y, fieldType):
        self.x = x
        self.y = y
        self.fieldType = fieldType
        self.flagged = False
        self.uncovered = False
    
    def checkField(self, x, y):
        if self.x == x and self.y == y:
            return True
        return False