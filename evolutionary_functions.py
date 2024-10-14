import random
from config import configGenetic
 
def paretoFrontWeighting(musicPopulation):
    weighting = []
 
    # Identify non-dominated individuals (Pareto front)
    for individual in musicPopulation:
        candidatesDominated = 0
        for competitor in musicPopulation:
            #if i isn't checking itself and dominates j, add 1 to domination number
            if individual != competitor and dominates(individual[1], competitor[1]):
                candidatesDominated += 1
        weighting.append(candidatesDominated + 1) #+1 to give chance to candidates who dominated no-one (adds minimized diversity)

    return weighting
 
# Helper function to check if one individual dominates another
def dominates(individualA, individualB, tolerance=0.01):
    try:
        better_in_all = all(float(a) >= float(b) - tolerance for a, b in zip(individualA.values(), individualB.values()))
        strictly_better_in_one = any(float(a) > float(b) + tolerance for a, b in zip(individualA.values(), individualB.values()))
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
    return child

def mutation_pitch_change(child, noteAmount, idx):
    bool = True
    attempts = 0
    child = child
    while bool and attempts < noteAmount:
        if child[idx-1][0] != 'rest':
            note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g'])[0]
            while note == child[idx-1][0]:
                note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g'])[0]
            #mutate child here
            child[idx-1][0] = note
            bool = False
        else:
            idx += 1
            attempts += 1
            if idx > noteAmount: 
                idx = 0

def mutation_rest_to_note(child, noteAmount, idx):
    bool = True
    attempts = 0
    while bool and attempts < noteAmount:
        if child[idx-1][0] == 'rest':
            note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g','C'])[0]
            #mutate child here
            child[idx-1][0] = note
            child[idx-1][1] = 'natural'
            bool = False
        else:
            idx += 1
            attempts += 1
            if idx > noteAmount: 
                idx = 0

def mutation_crotchet_to_rest(child, noteAmount, idx):
    bool = True
    attempts = 0
    while bool and attempts < noteAmount:
        if child[idx-1][2] == 'crotchet' and child[idx-1][0] != 'rest':
            #mutate child here
            child[idx-1][0] = 'rest'
            child[idx-1][1] = ''
            bool = False
        else:
            idx += 1
            attempts += 1
            if idx > noteAmount: 
                idx = 0

def mutation_split_note(child, noteAmount, idx):
    bool = True
    attempts = 0
    while bool and attempts < noteAmount:
        note = child[idx-1]
        #don't split crotchets or quavers as they are already small
        if note[2] != 'quaver'and note[2] != 'crotchet' and note[0] != 'rest':
            #mutate child here
            if note[2] == 'minim':
                note[2] = 'crotchet'
                child.insert(idx-1, note)
            if note[2] == 'dottedMinim':
                note[2] = 'crotchet'
                placement = random.randint(0,1)
                child.insert(idx-1+placement, [note[0], note[1], 'minim', note[3]])
            if note[2] == 'semibreve':
                note[2] = 'minim'
                child.insert(idx-1, note)
            bool = False
        else:
            idx += 1
            attempts += 1
            if idx > noteAmount: 
                idx = 0
# add mutation to combine and split notes