import pygame
import sys
import random
import time

screen_width = 1280
screen_height = 720

gridsize = 40
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = [0,-1]
down = [0,1]
left = [-1,0]
right = [1,0]

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [[int(screen_width/2), int(screen_height/2)]]
        self.direction = random.choice([up, down, left, right])
        self.color = (86,86,86)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        elif point != [-1*coord for coord in self.direction]:
            self.direction = point

    def check_death(self,head_pos):
        x,y = self.direction
        new = [int((head_pos[0]+(x*gridsize))%screen_width), int((head_pos[1]+(y*gridsize))%screen_height)]
        if len(self.positions) > 2 and new in self.positions[2:]:
            return 1
        elif head_pos[0] == 0 and self.direction == left:
            return 1
        elif head_pos[1] == 0 and self.direction == up:
            return 1
        elif head_pos[0] == screen_width - 40 and self.direction == right:
            return 1
        elif head_pos[1] == screen_height - 40 and self.direction == down:
            return 1
        else:
            return 0

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = [int((cur[0]+(x*gridsize))%screen_width), int((cur[1]+(y*gridsize))%screen_height)]
        if self.check_death(cur):
            #pygame.mixer.music.load('death_sound.mp3')
            #pygame.mixer.music.play(0)
            time.sleep(1)
            self.reset()
            return 1
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return 0

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (105,105, 105), r, 1)

    def random_movement(self, move):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if move == 0:
            self.turn(up)
        elif move == 1:
            self.turn(down)
        elif move == 2:
            self.turn(left)
        elif move == 3:
            self.turn(right)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = [0,0]
        self.color = (255, 255, 255)
        self.randomize_position()

    def randomize_position(self):
        self.position = [random.randint(1, grid_width-1)*gridsize, random.randint(1, grid_height-1)*gridsize]
        #self.position = [120,360]

    def draw(self, surface):
        #r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        #pygame.draw.rect(surface, self.color, r)
        #pygame.draw.rect(surface, (86,86,86), r, 2)
        pygame.draw.circle(surface, (255, 255, 255), (self.position[0]+20, self.position[1]+20), 20)
        pygame.draw.circle(surface, (86, 86, 86), (self.position[0]+20, self.position[1]+20), 20, 2)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(255,130,66), r)
