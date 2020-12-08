from game import *
from model import *
import time

def closest_to_head(snake, grid_height = 18, grid_width = 32):
    direction = snake.direction
    positions = snake.positions
    head = positions[0]
    temp = head
    if direction == up:
        for i in range(1,int(grid_height-head[1])+1):
            temp[1] -= 40.0
            if temp in positions:
                return i
    if direction == down:
        for i in range(1,int(grid_height-head[1])+1):
            temp[1] += 40.0
            if temp in positions:
                return i
    if direction == left:
        for i in range(1,int(grid_width-head[0])+1):
            temp[0] -= 40.0
            if temp in positions:
                return i
    if direction == right:
        for i in range(1,int(grid_height-head[0])+1):
            temp[0] += 40.0
            if temp in positions:
                return 40.0
    return 100
        

def generate_training(n_samples, moves_per_sample):
    for game in range(n_samples):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
        surface = pygame.Surface(screen.get_size())
        surface = surface.convert()
        clock.tick(10)
        drawGrid(surface)
        snake = Snake()
        food = Food()
        training_x = []
        training_y = []

        chromosome = [snake.positions[0][0], snake.positions[0][1],food.position[0],food.position[1],closest_to_head(snake),snake.direction]
        for _ in range(moves_per_sample):
            print(chromosome)
            time.sleep(0.1)
            training_x.append(chromosome)

            #if chromosome[4] <= 2:
            #    if chromosome[5] == up or chromosome[5] == down:
            #        turn = random.choice([left, right])
            #    else:
            #        turn = random.choice([up, down])
            #    snake.turn(turn)

            #If snake is to the left of food and snake is not moving towards or directly away(can't turn 180 degree)
            if chromosome[0] < chromosome[2] and snake.direction != left:
                #turn snake right
                snake.random_movement(3)
                training_y.append(3)
            elif chromosome[0] > chromosome[2] and snake.direction != right:
                #turn it left
                snake.random_movement(2)
                training_y.append(2)
            elif chromosome[1] > chromosome[3] and snake.direction != down:
                #turn it up
                snake.random_movement(0)
                training_y.append(0)
            elif chromosome[1] < chromosome[3] and snake.direction != up:
                #turn it down
                snake.random_movement(1)
                training_y.append(1)
            drawGrid(surface)
            dead = snake.move()
            if dead == 1:
                break
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                pygame.mixer.music.load('eat_sound.mp3')
                pygame.mixer.music.play(0)
                food.randomize_position()
            snake.draw(surface)
            food.draw(surface)
            chromosome = [snake.positions[0][0], snake.positions[0][1],food.position[0],food.position[1],closest_to_head(snake),snake.direction]
            screen.blit(surface, (0,0))
            pygame.display.update()

generate_training(10,1000)