from game_test import *
import random

def cummulative_probabilites(chromosomes, gen_scores):
    chromosomes = [chromosomes for _,chromosomes in sorted(zip(gen_scores,chromosomes))]
    gen_scores = sorted(gen_scores)
    sum_gen_scores = sum(gen_scores)
    if sum_gen_scores == 0:
        return chromosomes, gen_scores
    for i in range(len(gen_scores)):
        gen_scores[i] /= sum_gen_scores
    cumm_gen_scores = []
    add = 0
    for score in gen_scores:
        add += score
        cumm_gen_scores.append(add)
    
    return chromosomes, cumm_gen_scores

#! Accidental Elitism(Both parents same)
def natural_selection(cumm_gen_scores, n_pairs):
    parent_pairs = []
    if cumm_gen_scores[-1] == 0:
        return [[0,1],[2,3],[4,5],[6,7],[8,9]]
    for _ in range(n_pairs):
        parents = []
        for _ in range(2):
            pick = random.uniform(0,1)
            for i in range(len(cumm_gen_scores)):
                if cumm_gen_scores[i] > pick:
                    parents.append(i)
                    break
        parent_pairs.append(parents)
    return parent_pairs

def crossover(parent1, parent2):
    child1 = []
    child2 = []
    for i in range(len(parent1)):
        pick = random.randint(0,1)
        if pick == 0:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child2.append(parent1[i])
            child1.append(parent2[i])
    return child1, child2



def main():
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
        for _ in range(150):
            chromosome.append(random.randint(0,4))
        chromosomes.append(chromosome)

    for j in range(n_generations):
        gen_scores = []
        n_pairs = int(len(chromosomes)/2)
        for chromosome in chromosomes:
            snake.reset()
            food.randomize_position()
            for move in chromosome:
                clock.tick(10)
                #move = random.randint(0,3)
                snake.random_movement(move)
                drawGrid(surface)
                snake.move()
                if snake.get_head_position() == food.position:
                    snake.length += 1
                    snake.score += 1
                    pygame.mixer.music.load('eat_sound.mp3')
                    pygame.mixer.music.play(0)
                    food.randomize_position()
                snake.draw(surface)
                food.draw(surface)
                screen.blit(surface, (0,0))
                text = myfont.render("Score {0}\n Generation {1}".format(snake.score,j), 1, (0,0,0))
                screen.blit(text, (5,10))
                pygame.display.update()
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



        
        

        

        
                

main()