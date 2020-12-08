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
