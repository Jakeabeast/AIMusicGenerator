import music
import fitness
import random


def create_file(numMusic, numBars, fileName = "test"):
    rawData = music.UnrefinedMusic(bars = numBars)
    FILENAME = fileName + "File.txt"

    delete_file_content(fileName)

    file = open(FILENAME, 'a')
    file.write("\\version \"2.24.1\"\n")
    file.write("\header {{ title = \markup \"{0}\" }}\n".format(fileName))
    file.write("%Bar Length: {0}\n\n".format(numBars))
    file.close()

    for i in range(numMusic):
        rawData.set_seed(random.random())
        add_exercise(fileName, rawData, i)

def create_sorted_file(seeds, numBars, fileName = "test"):
    rawData = music.UnrefinedMusic(bars = numBars)
    fileName = "Sorted" + fileName
    FILENAME = fileName + "File.txt"
    
    delete_file_content(fileName)

    file = open(FILENAME, 'a')
    file.write("\\version \"2.24.1\"\n")
    file.write("\header {{ title = \markup \"{0}\" }}\n".format(fileName))
    file.write("%Bar Length: {0}\n\n".format(numBars))
    file.close()

    for i in range(len(seeds)):
        rawData.set_seed(seeds[i])
        add_exercise(fileName, rawData, i)


def delete_file_content(fileName):
    FILENAME = fileName + "File.txt"
    file_to_delete = open(FILENAME,'w')
    file_to_delete.close()

def add_exercise(fileName, rawData, iteration):
        FILENAME = fileName + "File.txt"
        file = open(FILENAME, 'a')
        file.write("%Music_Exercise_{0} - Seed: {1}\n".format(str(iteration+1), rawData.get_seed()))
        file.write("\markup \"Music_Exercise_{0}\"\n".format(str(iteration+1)))
        file.close()

        music.Lilypond(rawData, fileName)

        file = open(FILENAME, 'a')
        file.write("%\Fitness Test (Note:Rest)= {0}\n".format(fitness.note_rest_ratio(rawData)))
        file.write("%\Fitness Test (Note Length)= {0}\n".format(fitness.note_length_ratio(rawData)))
        file.write("%\Fitness Test (Melody)= {0}\n".format(fitness.contiguous_melody_ratio(rawData)))
        file.write("%\Fitness Test (Interval Size)= {0}\n".format(fitness.interval_size_ratio(rawData)))
        file.write("%\Fitness Test (Overall)= {0}\n\n\n".format(fitness.all_default_test(rawData)))
        file.close()

def sort_by_rank(fileName, fitnessTest):
    FILENAME = fileName + "File.txt"

    #safely get number of bars
    try:
        x = open(FILENAME, 'r').readlines()[2] #read from line 3 the bar number in FILENAME
        numBars = int(extract_float_from_line(x))
    except:
        print("CHECK INDEX OF \'%Bar Length: \#\' IN THE SORTED FILE")
    
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

    sorted_values = sorted(dictionary.values()) # Sort the values
    sorted_seeds = []

    prev = -1
    for i in sorted_values:
        if i == prev:
            continue
        prev = i
        for k in dictionary.keys():
            if dictionary[k] == i:
                sorted_seeds.append(k)
    
    sorted_seeds = list(reversed(sorted_seeds))
    create_sorted_file(seeds = sorted_seeds, numBars = numBars, fileName = fileName)


def extract_float_from_line(str):
    num = ""
    read = False
    for n in str:
        if n == ':' or n == '=':
            read = True

        if (n.isdigit() or n == ".") and read:
            num += n       
    return(float(num))