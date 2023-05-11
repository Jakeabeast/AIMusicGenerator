import music
import fitness
import random

def create_file(numMusic, numBars, fileName):
    rawData = music.UnrefinedMusic(bars = numBars)
    FILENAME = fileName + "File.txt"

    file = open(FILENAME, 'a')
    file.write("\\version \"2.24.1\"\n")
    file.write("\header {{ title = \markup \"{0}\" }}\n\n".format(fileName))
    file.close()

    for i in range(numMusic):

        rawData.set_seed(random.random())

        file = open(FILENAME, 'a')
        file.write("%Music_Exercise_{0} - Seed: {1}\n".format(str(i+1), rawData.get_seed()))
        file.write("\markup \"Music_Exercise_{0}\"\n".format(str(i+1)))
        file.close()

        music.Lilypond(rawData, fileName)

        file = open(FILENAME, 'a')
        file.write("%\Fitness Test (Note:Rest)= {0}\n".format(fitness.note_rest_ratio(rawData)))
        file.write("%\Fitness Test (Note Length)= {0}\n".format(fitness.note_length_ratio(rawData)))
        file.write("%\Fitness Test (Melody)= {0}\n".format(fitness.contiguous_melody_ratio(rawData)))
        file.write("%\Fitness Test (Interval Size)= {0}\n".format(fitness.interval_size_ratio(rawData)))
        file.write("%\Fitness Test (Overall)= {0}\n\n\n".format(fitness.all_default_test(rawData)))
        file.close()

def delete_file_content(fileName):
    FILENAME = fileName + "File.txt"
    file_to_delete = open(FILENAME,'w')
    file_to_delete.close()

def test_seed(seed):
    rawData = music.UnrefinedMusic(seed = seed)
    music.Lilypond(rawData)

if __name__ == "__main__":
    
    #test_seed(seed<-HERE)


    
    



    

    
