import music

if __name__ == "__main__":
    rawData = music.UnrefinedMusic(20, ["C", "major"], "treble", [4,4]) #overloading not working?
    rawLilypond = music.RawLilypond(rawData)
    textFile= music.EngravedLilypond(rawLilypond)
    
