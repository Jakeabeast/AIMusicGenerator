from music import UnrefinedMusic, Lilypond
from config import active_config as config
import fitness
import random

#global
fitness_scores = {
	"overall_score" : [],
	"note_rest_ratio": [],
	"note_length_ratio" : [],
	"contiguous_melody_ratio" : [],
	"interval_size_ratio" : []
}
overall_score_array = []

FILE_TYPE = ".txt"


def create_file(numMusic, numBars, fileName = "test", seed = None):
	FILENAME = fileName + FILE_TYPE

	file = open(FILENAME, 'w')
	file.write("\\version \"2.23.6\"\n")
	file.write("\\header {{ title = \"{0}\" }}\n".format(fileName))
	file.write("%Bar Length: {0}\n".format(numBars))
	file.write("%Configuration: {0}\n\n".format(config.print_config()))


	for i in range(numMusic):
		rawData = UnrefinedMusic(seed = seed, bars = numBars)
		score = add_exercise(file, fileName, rawData, i)
		overall_score_array.append(score)

	file.close()

def create_sorted_file(seeds, numBars, fitnessName, fileName = "test"):
	fileName = "SortedBy" + fitnessName + "-" + fileName 
	FILENAME = fileName + FILE_TYPE

	file = open(FILENAME, 'w')
	file.write("\\version \"2.24.1\"\n")
	file.write("\\header {{ title = \\markup \"{0}\" }}\n".format(fileName))
	file.write("%Bar Length: {0}\n\n".format(numBars))

	for i in range(len(seeds)):
		rawData = UnrefinedMusic(seed = seeds[i], bars = numBars)
		add_exercise(file, fileName, rawData, i)

	file.close()

#unecessary function for now as all new files should overwrite same file name
def delete_file_content(name):
	file_to_delete = open(name,'w')
	file_to_delete.close()

def add_exercise(file, fileName, rawData, iteration = 1):
		file.write("%Music_Exercise_{0} - Seed: {1}\n".format(str(iteration+1), rawData.seed_str()))
		file.write("\\markup \"Music_Exercise_{0}\"\n".format(str(iteration+1)))

		# write lilypond music into file (return string instead?)
		Lilypond(rawData, file, fileName)

		# write fitness scores + append to global dict
		note_rest_ratio = fitness.note_rest_ratio(rawData)
		fitness_scores["note_rest_ratio"].append(note_rest_ratio)
		file.write("%\\Fitness Test (NoteToRest)= {0}\n".format(fitness.note_rest_ratio(rawData)))

		note_length_ratio = fitness.note_length_ratio(rawData)
		fitness_scores["note_length_ratio"].append(note_length_ratio)
		file.write("%\\Fitness Test (NoteLength)= {0}\n".format(fitness.note_length_ratio(rawData)))
		
		contiguous_melody_ratio = fitness.contiguous_melody_ratio(rawData)
		fitness_scores["contiguous_melody_ratio"].append(contiguous_melody_ratio)
		file.write("%\\Fitness Test (Melody)= {0}\n".format(fitness.contiguous_melody_ratio(rawData)))
		
		interval_size_ratio = fitness.interval_size_ratio(rawData)
		fitness_scores["interval_size_ratio"].append(interval_size_ratio)
		file.write("%\\Fitness Test (IntervalSize)= {0}\n".format(fitness.interval_size_ratio(rawData)))
		
		overall_score = fitness.all_default_test(rawData)
		fitness_scores["overall_score"].append(overall_score)
		file.write("%\\Fitness Test (Overall)= {0}\n\n\n".format(overall_score))
		return overall_score

def sort_by_rank(fitnessTest, fileName = "test"):
	FILENAME = fileName + FILE_TYPE

	#safely get number of bars
	try:
		#read from line 3 the bar number in FILENAME
		x = open(FILENAME, 'r').readlines()[2] 
		numBars = int(extract_float_from_line(x))
	except:
		print("CHECK INDEX OF \'%Bar Length: #\' IN THE SORTED FILE")
	
	#creat dictionary with seed:rank mapping
	dictionary = {}
	with open(FILENAME, 'r') as file:
		lines = file.readlines()
		i = 0
		key = True
		for row in lines:
			if row.find('Seed') != -1 or row.find(fitnessTest) != -1:
				num = extract_float_from_line(row)
				if key: 
					seed = num
					key = False
				else: 
					rank = num
					key = True
					dictionary[seed] = rank
			i += 1

	#Sort the values
	sorted_values = sorted(dictionary.values()) 
	sorted_seeds = []
	prev = -1
	for i in sorted_values:
		#if multiple of same seed, skip
		if i == prev:
			continue
		prev = i

		for k in dictionary.keys():
			if dictionary[k] == i:
				sorted_seeds.append(k)
				continue
	sorted_seeds = list(reversed(sorted_seeds))

	create_sorted_file(seeds = sorted_seeds, numBars = numBars, fitnessName = fitnessTest, fileName = fileName)

#read float number from string line
def extract_float_from_line(str):
	num = ""
	read = False
	for n in str:
		if n == ':' or n == '=':
			read = True

		if (n.isdigit() or n == ".") and read:
			num += n
	return(float(num))