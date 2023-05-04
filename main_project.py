import music
import fitness

if __name__ == "__main__":
    rawData = music.UnrefinedMusic() 
    print(rawData.get_notes())
    print("\nTEST\n")
    print(fitness.note_rest_ratio(rawData), end="\n")
    print(fitness.note_length_ratio(rawData), end="\n")
    print(fitness.contiguous_melody_ratio(rawData), end="\n")    
    print(fitness.interval_size_ratio(rawData), end="\n\n")
    print(fitness.all_default_test(rawData), end="\n")

    print("\nTEST\n")
    Lilypond = music.Lilypond(rawData)
    

    
