import pygame

import math
import time

from collections import deque
from mouse import Mouse
from cat import Cat

class Game:

    def __init__(self):
        pygame.init()

        self.load_images()
        self.create_map()

        self.height = len(self.map)
        self.width = len(self.map[0])
        self.scale = self.images[0].get_width()

        self.mouse = Mouse(int(self.width/2), int(self.height/2))
        self.create_cats()
        self.set_cats()
        self.game_over = False

        display_height = self.scale * self.height
        display_width = self.scale * self.width
        self.display = pygame.display.set_mode((display_width, display_height))

        pygame.display.set_caption("Game")

        self.loop()

    def load_images(self):
        self.images = []
        for name in ["empty", "tile", "mouse", "cat"]:
            self.images.append(pygame.image.load("src/" + name + ".png"))

    # def new_game(self):
    #     self.map = [[0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    #                 [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    #                 [0, 3, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    #                 [0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 0],
    #                 [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    #                 [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    #                 [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],]

    # def find_mouse(self):
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             if self.map[y][x] == 2:
    #                 return (x, y)
    
    def create_map(self):
        height = 17
        width = 15
        middle_start_y = math.floor(height/4)
        middle_start_x = math.floor(width/4)
        self.map = []

        for i in range(0, height):
            list = []
            for j in range(0, width):
                if ((middle_start_x - 1) < j < (width - middle_start_x)) & ((middle_start_y - 2) < i < (height + 1) - middle_start_y):
                    list.append(1)
                else: list.append(0)
            self.map.append(list)
        self.map[math.floor(height/2)][math.floor(width/2)] = 2
    
    def create_cats(self):
        self.cats = []
        self.cats.append(Cat(int(self.width/2), 1))
        self.cats.append(Cat(int(self.width/2), int(self.height - 2)))
        self.cats.append(Cat(1, int(self.height/2)))
        self.cats.append(Cat(int(self.width - 2), int(self.height/2)))
    
    def set_cats(self):
        for cat in self.cats:
            self.map[cat.y][cat.x] = 3
        
    def move_cats(self):
        distances = self.get_distances()
        for cat in self.cats:
            self.map[cat.y][cat.x] = 0
            cat.set_new_location(self.map, distances, self.mouse.x, self.mouse.y)
            self.map[cat.y][cat.x] = 3
    
    def run_into_cat(self, x, y):
        if self.map[y][x] == 3:
            self.game_over = True
            return True
        return False
    
    def get_distances(self):
        queue = deque()
        handled = [[False for x in range(len(self.map[0]))] for y in range(len(self.map))]
        distances = [[0 for x in range(len(self.map[0]))] for y in range(len(self.map))]

        mousey = self.mouse.y
        mousex = self.mouse.x

        queue.append((mousey, mousex))
        handled[mousey][mousex] = True
        distances[mousey][mousex] = 0
        
        while len(queue) > 0:
            place = queue.popleft()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if place[0] + i < 0 or place[0] + i > len(self.map) - 1 or place[1] + j < 0 or place[1] + j > len(self.map[0]) - 1:
                        continue
                    if handled[place[0] + i][place[1] + j]:
                        new_distance = distances[place[0]][place[1]] + 1
                        if self.map[place[0]][place[1]] != 1 and self.map[place[0] + i][place[1] + j] != 1 and new_distance < distances[place[0] + i][place[1] + j]:
                            distances[place[0] + i][place[1] + j] = new_distance
                            queue.append((place[0] + i, place[1] + j))
                        continue
                    if self.map[place[0] + i][place[1] + j] == 1:
                        distances[place[0] + i][place[1] + j] += 100
                    queue.append((place[0] + i, place[1] + j))
                    handled[place[0] + i][place[1] + j] = True
                    distances[place[0] + i][place[1] + j] += distances[place[0]][place[1]] + 1
        print("Etäisyydet: ")
        for line in distances:
            print(line)
        return distances

    def loop(self):
        cat_timer = 0
        while not self.game_over:
            cat_timer += 1
            fps = 60
            time.sleep(1/fps)
            self.check_events()
            if cat_timer >= 60:
                self.move_cats()
                self.run_into_cat(self.mouse.x, self.mouse.y)
                cat_timer = 0
            self.draw_display()

        self.display.fill((0, 0, 0))
        pygame.display.flip()

    def check_events(self):
        for happening in pygame.event.get():
            if happening.type == pygame.QUIT:
                exit()
            if happening.type == pygame.KEYDOWN:
                if happening.key == pygame.K_LEFT:
                    self.move_left()
                if happening.key == pygame.K_RIGHT:
                    self.move_right()
                if happening.key == pygame.K_UP:
                    self.move_up()
                if happening.key == pygame.K_DOWN:
                    self.move_down()

    def move_left(self):
        old_x = self.mouse.x
        new_x = old_x - 1
        
        if not self.can_move(new_x, self.mouse.y):
            return
        # if self.run_into_cat(new_x, self.mouse.y):
        #     return
        if not self.move_tiles_left(new_x, self.mouse.y):
            return

        self.mouse.move_left()
        self.map[self.mouse.y][old_x] = 0
        self.map[self.mouse.y][new_x] = 2

    def move_right(self):
        old_x = self.mouse.x
        new_x = old_x + 1
        
        if not self.can_move(new_x, self.mouse.y):
            return
        # if self.run_into_cat(new_x, self.mouse.y):
        #     return
        if not self.move_tiles_right(new_x, self.mouse.y):
            return

        self.mouse.move_right()
        self.map[self.mouse.y][old_x] = 0
        self.map[self.mouse.y][new_x] = 2

    def move_up(self):
        old_y = self.mouse.y
        new_y = old_y - 1

        if not self.can_move(self.mouse.x, new_y):
            return
        # if self.run_into_cat(self.mouse.x, new_y):
        #     return
        if not self.move_tiles_up(self.mouse.x, new_y):
            return
        
        self.mouse.move_up()
        self.map[old_y][self.mouse.x] = 0
        self.map[new_y][self.mouse.x] = 2

    def move_down(self):
        old_y = self.mouse.y
        new_y = old_y + 1

        if not self.can_move(self.mouse.x, new_y):
            return
        # if self.run_into_cat(self.mouse.x, new_y):
        #     return
        if not self.move_tiles_down(self.mouse.x, new_y):
            return
        
        self.mouse.move_down()
        self.map[old_y][self.mouse.x] = 0
        self.map[new_y][self.mouse.x] = 2
        
    def can_move(self, x, y):
        if x < 0 or x > self.width:
            return False
        if y < 0 or y > self.height:
            return False
        return True

    def move_tiles_left(self, x, y):
        if self.map[y][x] == 0:
            return True
        i = 1
        if x - i == -1 :
            return False
        while self.map[y][x - i] == 1:
            i += 1
            if x - i == -1:
                return False
        if self.map[y][x - i] == 3:
            return False
        self.map[y][x - i] = 1
        return True

    def move_tiles_right(self, x, y):
        if self.map[y][x] == 0:
            return True
        i = 1
        if x + i > self.width - 1:
            return False
        while self.map[y][x + i] == 1:
            i += 1
            if x + i > self.width - 1:
                return False
        if self.map[y][x + i] == 3:
            return False
        self.map[y][x + i] = 1
        return True
    
    def move_tiles_up(self, x, y):
        if self.map[y][x] == 0:
            return True
        i = 1
        if y - i == -1:
            return False
        while self.map[y - i][x] == 1:
            i += 1
            if y - i == -1:
                return False
        if self.map[y - i][x] == 3:
            return False
        self.map[y - i][x] = 1
        return True
    
    def move_tiles_down(self, x, y):
        if self.map[y][x] == 0:
            return True
        i = 1
        if y + i > self.height - 1:
            return False
        while self.map[y + i][x] == 1:
            i += 1
            if y + i > self.height - 1:
                return False
        if self.map[y + i][x] == 3:
            return False
        self.map[y + i][x] = 1
        return True

    def draw_display(self):
        self.display.fill((0, 0, 0))

        for y in range(self.height):
            for x in range(self.width):
                tile = self.map[y][x]
                self.display.blit(self.images[tile], (x * self.scale, y * self.scale))
            
        pygame.display.flip()
    

# if __name__ == "__main__":
#     Game()