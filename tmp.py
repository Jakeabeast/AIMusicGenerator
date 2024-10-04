import random
from config import configGenetic
 
#function that accepts 2 "chromosomes" (pieces of music) and combines their genes to see if the result is greater or not
def paretoSelection(musicPopulation):
    pareto_front = []
   
 
    # Identify non-dominated individuals (Pareto front)
    for i, individual in enumerate(musicPopulation):
        dominated = False
        for j, competitor in enumerate(musicPopulation):
            if i != j and dominates(individual[1], competitor[1]):
                dominated = True
                break
        if not dominated:
            pareto_front.append(individual)
 
    # Randomly select two individuals from the Pareto front
    if len(pareto_front) >= 2:
        return random.sample(pareto_front, 2)
    else:
        return random.sample(musicPopulation, 2)
 
# Helper function to check if one individual dominates another
def dominates(individualA, individualB):
    better_in_all = all(a >= b for a, b in zip(individualA, individualB))
    strictly_better_in_one = any(a > b for a, b in zip(individualA, individualB))
    return better_in_all and strictly_better_in_one
 
#function accepts 2 parent music, mixes their genes to create new children with their fitness values
def uniformCrossOver(parent1, parent2):
    child1Notes = []
    child2Notes = []
 
    p1idx = 0
    p2idx = 0
    barIdx = 1
 
    #distribute genes from 2 parents into 2 children
    while barIdx <= configGenetic["numberBars"]:
        #50% chance to copy music at barIdx from one parent or the other
        if random.randint(0,1) == 1:
            while p1idx < len(parent1) and barIdx == parent1[p1idx][3]:
                child1Notes.append(parent1[p1idx])
                p1idx += 1
            while p2idx < len(parent2) and barIdx == parent2[p2idx][3]:
                child2Notes.append(parent2[p2idx])
                p2idx += 1
        else:
            while p1idx < len(parent1) and barIdx == parent1[p1idx][3]:
                child2Notes.append(parent1[p1idx])
                p1idx += 1
            while p2idx < len(parent2) and barIdx == parent2[p2idx][3]:
                child1Notes.append(parent2[p2idx])
                p2idx += 1
 
        barIdx += 1
    return child1Notes, child2Notes
 
#function mutates a piece of music and adjusts fitness
def mutatePiece(child):
    noteAmount = len(child)
    idx = random.randint(0, noteAmount - 1)
 
    allMutations = []
    for name, func in globals().items():
        if callable(func) and name.startswith('mutation_'):
            allMutations.append(func)
    random.choice(allMutations)(child, noteAmount, idx)
 
def mutation_pitch_change(child, noteAmount, idx):
    mutationType = random.randint(0, 4)
    #change note to different pitch
    if mutationType == 0:
        bool = True
        while bool:
            if child[idx-1][0] != 'rest':
                note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g'])[0]
                while note == child[idx][0]:
                    note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g'])[0]
                bool = False
            else:
                idx += 1
                if idx > noteAmount: 
                    idx = 0