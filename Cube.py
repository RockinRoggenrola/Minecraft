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
            (x, y+1, z),
            (x, y+1, z+1),
            (x, y, z+1),
            (x+1, y, z+1),
            (x+1, y+1, z+1)
        )

    def edges(self):
        return (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (7, 2),
            (6, 1),
            (5, 0)
        )