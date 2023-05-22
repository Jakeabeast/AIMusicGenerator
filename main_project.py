import music
import fitness
import database


def test_seed(seed):
    rawData = music.UnrefinedMusic(seed = seed)
    music.Lilypond(rawData)
    print("Fitness Test (Note:Rest)= {0}\n".format(fitness.note_rest_ratio(rawData)))
    print("Fitness Test (Note Length)= {0}\n".format(fitness.note_length_ratio(rawData)))
    print("Fitness Test (Melody)= {0}\n".format(fitness.contiguous_melody_ratio(rawData)))
    print("Fitness Test (Melody Test) [Allow same pitch x2]= {0}\n".format(fitness.testcontiguous_melody_ratio(rawData)))
    print("Fitness Test (Interval Size)= {0}\n".format(fitness.interval_size_ratio(rawData)))
    print("Fitness Test (Overall)= {0}\n\n\n".format(fitness.all_default_test(rawData)))


def extract_float_from_line(str):
    num = ""
    read = False
    for n in str:
        if n == ':':
            read = True

        if (n.isdigit() or n == ".") and read:
            num += n
    print(str, end="")
    print(num, end="\n")        
    return(float(num))

    


if __name__ == "__main__":
    
    
   database.create_file(40, 8, "UnweightedExercises")
   database.sort_by_rank("UnweightedExercises", "NoteToRest")
   database.sort_by_rank("UnweightedExercises", "NoteLength")
   database.sort_by_rank("UnweightedExercises", "Melody")
   database.sort_by_rank("UnweightedExercises", "IntervalSize")
   database.sort_by_rank("UnweightedExercises", "Overall")

    
