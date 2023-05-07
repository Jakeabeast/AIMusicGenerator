import music
import fitness

if __name__ == "__main__":
    rawData = music.UnrefinedMusic(0.6978718329447697, bars = 4) 
    print(rawData.get_notes())
    print("Seed: "+ str(rawData.get_seed()))
    print("\nFITNESS TEST\n")
    print(fitness.note_rest_ratio(rawData), end="\n")
    print(fitness.note_length_ratio(rawData), end="\n")
    print(fitness.contiguous_melody_ratio(rawData), end="\n")    
    print(fitness.interval_size_ratio(rawData), end="\n\n")
    print(fitness.all_default_test(rawData), end="\n")

    print("\nFITNESS TEST\n")
    Lilypond = music.Lilypond(rawData)
    

    
