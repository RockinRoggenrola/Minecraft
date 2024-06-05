class Cube:
    def __init__(self, x, y, z, color):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
    
    def vertices(self):
        x = self.x
        y = self.y
        z = self.z
        return (
            (x, y, z),
            (x+1, y, z),
            (x+1, y+1, z),
            (x+1, y+1, z+1),
            (x, y+1, z+1),
            (x, y, z+1),
            (x, y+1, z+1),
            (x, y+1, z)
        )

    def edges():
        return (
            (0, 1),
            (0, 5),
            (0, 7),
            (2, 7),
            (2, 1),
            (2, 3),
            (4, 3),
            (4, 5),
            (4, 7),
            (6, 5),
            (6, 7),
            (6, 4)
        )