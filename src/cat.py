from collections import deque
from math import inf

class Cat:

    def __init__(self, cox, coy):
        self.x = cox
        self.y = coy
        self.alive = True

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1
    
    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def find_cat(self):
        return self.x, self.y
    
    def set_new_location(self, map, distances, mousex, mousey):
        places = self.get_possible_spaces(map)

        min_distance = distances[self.y][self.x]
        miny, minx = self.y, self.x
        for place in places:
            new_distance = distances[place[1]][place[0]]
            if map[place[1]][place[0]] == 2:
                self.x, self.y = place[0], place[1]
                return
            if map[place[1]][place[0]] == 3:
                continue
            if new_distance < min_distance:
                if map[place[1]][place[0]] == 0:
                    min_distance = new_distance
                    miny, minx = place[1], place[0]

        self.x, self.y = minx, miny

    def get_possible_spaces(self, map):
        places = []
        if self.x - 1 >= 0:
            places.append((self.x - 1, self.y))
        if self.y - 1 >= 0:
            places.append((self.x, self.y - 1))
        if self.x + 1 <= len(map[0]) - 1 and self.y -1 >= 0:
            places.append((self.x + 1, self.y - 1))
        if self.x - 1 >= 0 and self.y + 1 <= len(map) - 1:
            places.append((self.x - 1, self.y + 1))
        if self.x - 1 >= 0 and self.y - 1 >= 0:
            places.append((self.x - 1, self.y - 1))
        if self.x + 1 <= len(map[0]) - 1:
            places.append((self.x + 1, self.y))
        if self.x + 1 <= len(map[0]) - 1 and self.y + 1 <= len(map) - 1:
            places.append((self.x + 1, self.y + 1))
        if self.y + 1 <= len(map) - 1:
            places.append((self.x, self.y + 1))

        return places

