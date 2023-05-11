import music
import fitness
import random

def create_database(numMusic, numBars, Name):
    rawData = music.UnrefinedMusic(bars = numBars)
    FILENAME = Name + "File.txt"

    file = open(FILENAME, 'a')
    file.write("\\version \"2.24.1\"\n")
    file.write("\header { title = \markup \"Database\" }\n\n")
    file.close()

    for i in range(numMusic):
        file = open(FILENAME, 'a')
        file.write("%Music_Exercise_{0}\n".format(str(i+1)))
        file.write("\markup \"Music_Exercise_{0}\"\n".format(str(i+1)))
        file.close()

        rawData.set_seed(random.random())
        music.Lilypond(rawData, FILENAME)

        file = open(FILENAME, 'a')
        file.write("%\Fitness Test (Note:Rest)= {0}\n".format(fitness.note_rest_ratio(rawData)))
        file.write("%\Fitness Test (Note Length)= {0}\n".format(fitness.note_length_ratio(rawData)))
        file.write("%\Fitness Test (Melody)= {0}\n".format(fitness.contiguous_melody_ratio(rawData)))
        file.write("%\Fitness Test (Interval Size)= {0}\n".format(fitness.interval_size_ratio(rawData)))
        file.write("%\Fitness Test (Overall)= {0}\n\n".format(fitness.all_default_test(rawData)))
        file.close()

if __name__ == "__main__":
     
    create_database(20, 8,"musicDatabase")



    

    
