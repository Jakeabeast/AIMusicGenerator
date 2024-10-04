import random
from config import configGenetic
 
def paretoSelection(musicPopulation, elitism_rate=0.1):
    pareto_front = []
 
    # Calculate fitness values from the musicPopulation
    fitnessValues = []
    for musicPiece in musicPopulation:
        fitnessValues.append(musicPiece[1])  # Assuming musicPiece[1][0] holds the fitness score or values
 
    population_size = len(musicPopulation)
    num_elites = max(1, int(elitism_rate * population_size))
 
    # Identify non-dominated individuals (Pareto front)
    for i, individual in enumerate(musicPopulation):
        dominated = False
        for j, competitor in enumerate(musicPopulation):
            if i != j and dominates(fitnessValues[j], fitnessValues[i]):
                dominated = True
                break
        if not dominated:
            pareto_front.append(individual)
 
    # Select elites based on overall fitness score (for stability)
    sorted_population = sorted(musicPopulation, key=lambda ind: ind[1]["overall_score"], reverse=True)
    elites = sorted_population[:num_elites]
 
    # Select additional individuals from the Pareto front
    pareto_selection_size = max(0, 2 - num_elites)
    if len(pareto_front) >= pareto_selection_size:
        selected_from_pareto = random.sample(pareto_front, pareto_selection_size)
    else:
        selected_from_pareto = random.sample(musicPopulation, pareto_selection_size)
 
    # Return the elites combined with individuals from the Pareto front
    return elites + selected_from_pareto
 
# Helper function to check if one individual dominates another
def dominates(individualA, individualB, tolerance=0.01):
    try:
        better_in_all = all(float(a) >= float(b) - tolerance for a, b in zip(individualA, individualB))
        strictly_better_in_one = any(float(a) > float(b) + tolerance for a, b in zip(individualA, individualB))
    except ValueError:
        print(f"Non-numeric value found in {individualA} or {individualB}")
        return False
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