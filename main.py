from music_generation import generate_initial_population
from evolutionary_functions import paretoFrontWeighting, uniformCrossOver, mutatePiece
from music_conversion import Lilypond
from fitness import all_default_tests
import music_file
from config import configGenetic
import graph
import copy

import random
import numpy as np

if __name__ == "__main__":
	#generate inital sorted population
	newPopulation = generate_initial_population(configGenetic)
	newPopulation.sort(key = lambda x: x[1]["overall_score"], reverse=True)

	unsuccessfulGenerations = 0
	bestCandidateScore = newPopulation[0][1]["overall_score"]

	#repeat workflow until no improvement is found in newerGenerations
	while unsuccessfulGenerations < configGenetic["terminationNumber"]:# and bestCandidateScore < configGenetic["terminationQuality"]:
		#copy previous population into this generations "oldPopulation"
		oldPopulation = newPopulation
		newPopulation = []
		paretoFront = None

		#add elites into new population
		for i in range(configGenetic["numberElites"]):
			newPopulation.append(oldPopulation[i])

		while len(newPopulation) <= configGenetic["populationSize"]:
			#paretoFront only created once per generation
			if not paretoFront:
				paretoFront= paretoFrontWeighting(oldPopulation)
				allWeights = 0
				for weight in paretoFront:
					allWeights += weight
				for i, weight in enumerate(paretoFront):
					paretoFront[i] = weight / allWeights
			#select parents from previous population using the paretoFront weighting (without replacement)
			pIdx = 	np.random.choice(range(len(oldPopulation)), size=2, replace=False, p=paretoFront)
			pIdx = pIdx.tolist()
			parent1 = oldPopulation[pIdx[0]]
			parent2 = oldPopulation[pIdx[0]]

			#do crossover on parents to create children (only note array of children)
			child1, child2 = uniformCrossOver(parent1[0]["noteArray"], parent2[0]["noteArray"])

			#percent chance to mutate either child (only note array of children)
			if random.randint(1,100) <= configGenetic["mutationChance"]:
				child1 = mutatePiece(copy.deepcopy(child1))
				pass
			if random.randint(1,100) <= configGenetic["mutationChance"]:
				child2 = mutatePiece(copy.deepcopy(child2))

			#assumes standard consistent musical characteristics
			child1 = {
						"bars" : configGenetic["numberBars"],
						"keySig" : ["C", "major"],
						"clef" : "treble",
						"timeSig" : [4, 4],
						"noteArray": child1
						}
			child2 = {
						"bars" : configGenetic["numberBars"],
						"keySig" : ["C", "major"],
						"clef" : "treble",
						"timeSig" : [4, 4],
						"noteArray": child2
						}

			if len(newPopulation) >= 87:
				pass

			child1Fitness = all_default_tests(child1)
			child2Fitness = all_default_tests(child2)

			#add children to end of newPopulation in correct format
			newPopulation.append([child1, child1Fitness])
			newPopulation.append([child2, child2Fitness])

		newPopulation.sort(key = lambda x: x[1]["overall_score"], reverse=True)

		#if there is no improvement to bestCandidate, then new generation is unsuccessful
		bestNewGenScore = newPopulation[0][1]["overall_score"]
		if bestCandidateScore == bestNewGenScore :
			unsuccessfulGenerations += 1
		else: 
			unsuccessfulGenerations = 0
			bestCandidateScore = bestNewGenScore 

	#best Candidate is first item in newPopulation which is sorted by overall_fitness_score
	bestCandidate = newPopulation[0]

	obj = Lilypond(bestCandidate)
	text = obj.format()
	print(text)

	if all_default_tests(bestCandidate[0]) != bestCandidate[1]:
		actualscore = all_default_tests(bestCandidate[0])
		scoreShown = bestCandidate[1]
		assert("error, likely mutation issue")

	#draw graph of created file
	graph.draw()