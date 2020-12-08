from game import *
from model import *

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

surface = pygame.Surface(screen.get_size())
surface = surface.convert()
drawGrid(surface)

snake = Snake()
food = Food()

myfont = pygame.font.SysFont("monospace",32)

n_generations = 50
n_chromosomes = 25
chromosomes = []
for _ in range(n_chromosomes):
    chromosome = []
    for _ in range(500):
        chromosome.append(random.randint(0,4))
    chromosomes.append(chromosome)

max_score = [0,0]
for j in range(n_generations):
    gen_scores = []
    n_pairs = int(len(chromosomes)/2)
    for chromosome in chromosomes:
        snake.reset()
        food.randomize_position()
        n_move = 1
        for move in chromosome:
            clock.tick(10)
            #move = random.randint(0,3)
            #snake.random_movement(move)
            snake.handle_keys()
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
            screen.blit(surface, (0,0))
            text = myfont.render("Score {0}\n Generation {1} {2}".format(snake.score,j,n_move), 1, (0,0,0))
            n_move += 1
            screen.blit(text, (5,10))
            pygame.display.update()
        if snake.score > max_score[0]:
            max_score[0] = snake.score
            max_score[1] = j
        gen_scores.append(snake.score)
    #?elitism
    
    #Roulette Wheel/Natural Selection
    chromosomes, gen_scores = cummulative_probabilites(chromosomes, gen_scores)
    parent_pairs = natural_selection(gen_scores, n_pairs)

    print(parent_pairs)

    chromosomes2 = []
    for pair in parent_pairs:
        chromosomes2.extend(crossover(chromosomes[pair[0]],chromosomes[pair[1]]))
    chromosomes = chromosomes2       

print(max_score)

