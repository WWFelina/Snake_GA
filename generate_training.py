from game import *
from model import *
import time
import csv

def greedy_mover(chromosome, direction):
        #If snake is to the left of food and snake is not moving towards or directly away(can't turn 180 degree)
    if chromosome[0] < chromosome[2] and direction != left:
        #turn snake right
        return 3
    elif chromosome[0] > chromosome[2] and direction != right:
        #turn it left
        return 2
    elif chromosome[1] > chromosome[3] and direction != down:
        #turn it up
        return 0
    elif chromosome[1] < chromosome[3] and direction != up:
        #turn it down
        return 1
    else:
        if direction == up:
            return 0
        elif direction == down:
            return 1
        elif direction == left:
            return 2
        else:
            return 3

def prevent_death(snake,chromosome):
    pos = chromosome[:2]
    if snake.check_eat(pos) != 0:
        moves = [down, up, left, right]
        moves_not_allowed = snake.check_eat(pos)
        for move in moves:
            if move not in moves_not_allowed:
                snake.turn(move)
                return 1, move
            
    if snake.check_death(pos) == 1 or snake.check_death(pos) == 2:
        if snake.direction == up or snake.direction == down:
            if pos[0] < chromosome[2]:
                snake.turn(right)
                return 1, right
            else:
                snake.turn(left)
                return 1, left
        else:
            if pos[1] < chromosome[3]:
                snake.turn(down)
                return 1, down
            else:
                snake.turn(up)
                return 1, up
                

    return 0, snake.direction

def generate_training(moves_per_sample):
    training_x = []
    training_y = []
   
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    clock.tick(10)
    drawGrid(surface)
    snake = Snake()
    food = Food()
    score_list = []
    chromosome = [snake.positions[0][0], snake.positions[0][1],food.position[0],food.position[1]]
    for _ in range(moves_per_sample):
        #time.sleep(0.2)
        drawGrid(surface)
        training_x.append(chromosome)
        dead, move = prevent_death(snake,chromosome)
        if not (dead):
            moves = greedy_mover(chromosome,snake.direction)
            snake.random_movement(moves)
            training_y.append(moves)
        else:
            if move == up:
                training_y.append(0)
            elif move == down:
                training_y.append(1)
            elif move == left:
                training_y.append(2)
            else:
                training_y.append(3)
        score = snake.score   
        death = snake.move()
        if death:
            score_list.append(score)
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            #pygame.mixer.music.load('eat_sound.mp3')
            #pygame.mixer.music.play(0)
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        chromosome = [snake.positions[0][0], snake.positions[0][1],food.position[0],food.position[1]]
        screen.blit(surface, (0,0))
        pygame.display.update()
    score_list.append(score)
    return training_x, training_y,score_list

x, y,score_list = generate_training(50000)

print(f"The snake played {len(score_list)} games")
print(f"The average score achieved by the snake was {sum(score_list)/(len(score_list))}")

with open('data.csv','w', newline='') as f:
    for i in range(len(x)):
        write = csv.writer(f)
        write.writerow(x[i]+[y[i]])

