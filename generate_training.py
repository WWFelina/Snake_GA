from game import *
from model import *
import time

def hamiltonian_mover(chromosome, snake):
    head_pos = snake.positions[0]
    body_pos = snake.positions[1:]
    food_pos = [chromosome[2], chromosome[3]]
    move_list = []
    traversed_tiles = [head_pos]
    moves = [up, down, left, right]
    while True:
        head_pos = traversed_tiles[-1]
        temp = [-1,-1,-1,-1]
        for i in range(len(moves)):
            new = [int((head_pos[0]+(moves[i][0]*gridsize))%screen_width), int((head_pos[1]+(moves[i][1]*gridsize))%screen_height)]
            if new not in body_pos and new not in traversed_tiles:
                dist_from_food = abs(new[0] - food_pos[0]) + abs(new[1] - food_pos[1])
                temp[i] = (dist_from_food)
        max_turn = temp.index(max(temp))
        move_list.append(moves[max_turn])
        made_turn = [int((head_pos[0]+(moves[max_turn][0]*gridsize))%screen_width), int((head_pos[1]+(moves[max_turn][1]*gridsize))%screen_height)]
        traversed_tiles.append(made_turn)
        print(moves[max_turn])
        if max(temp) == 0:
            return move_list
            break


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
    if snake.check_death(pos):
        if snake.direction == up or snake.direction == down:
            if pos[0] < screen_width/2:
                snake.turn(right)
            else:
                snake.turn(left)
            return 1
        else:
            if pos[1] < screen_height/2:
                snake.turn(down)
            else:
                snake.turn(up)
            return 1
    return 0

def generate_training(n_samples, moves_per_sample):
    training_x = []
    training_y = []
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

        chromosome = [snake.positions[0][0], snake.positions[0][1],food.position[0],food.position[1]]
        for _ in range(moves_per_sample):
            time.sleep(0.1)
            drawGrid(surface)
            training_x.append(chromosome)
            if not (prevent_death(snake,chromosome)):
                if snake.length < 4:
                    move = greedy_mover(chromosome,snake.direction)
                    snake.random_movement(move)
                    training_y.append(move)
                else:
                    move = hamiltonian_mover(chromosome)
                    snake.random_movement(move)
                    training_y.append(move)

            snake.move()
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
    return training_x, training_y

generate_training(1,500)
