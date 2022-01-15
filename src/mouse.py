class Mouse:

    def __init__(self, cox, coy):
        self.x = cox
        self.y = coy

    def move(self, x, y):
        self.x += x
        self.y += y

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1
    
    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def find_mouse(self):
        return self.x, self.y