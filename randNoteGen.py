import random

class MusicCreator:
    def __init__ (self, bars):
        self.BARS = bars
        self.timeSignature = [4,4] #in common time
        self.lengthByTimeSig = BARS * self.timeSignature[1]
        self.musicNotes = ["a", "b", "c", "d", "e", "f", "g"]

    def random_note(self):
        return random.choice(self.musicNotes)
    
    def convert_for_lilypond(self, note, noteDuration):
        if (noteDuration == 3): #convert to dotted note
            string = note + "\'2."
        else:
            durationNotation = int(noteDuration ** -1 * self.timeSignature[1])
            string = note + "\'" + str(durationNotation)
            
        return string
            

    def print_musical_list(self):
        
        remainingSong = self.lengthByTimeSig 
        remainingBar = self.timeSignature[1]

        print("{ ", end=" ")

        while remainingSong > 0:
            note = self.random_note()
            noteLength = random.choices([4,2,1], weights=(14,28,58)) # 1 = whole, 2 = half, 4 = quarter
            noteLength = noteLength[0]

            if noteLength > remainingSong: #does it fit at the end of bar
                continue
            elif noteLength > remainingBar: #note needs to beam over bar (spagetti for now)
                print(self.convert_for_lilypond(note, remainingBar) + "~ " 
                      + self.convert_for_lilypond(note, noteLength - remainingBar), end="  ")
                remainingBar = self.timeSignature[1] - (noteLength - remainingBar)
            else:
                
                print(self.convert_for_lilypond(note, noteLength), end="  ")          
                remainingBar -= noteLength
                if remainingBar <= 0:
                    remainingBar = self.timeSignature[1]

            remainingSong -= noteLength
        #print(self.durationList) #to view list in terminal
            
        print("} ", end=" ") 


if __name__ == "__main__":
    BARS = 8 #input number of bars

    test = MusicCreator(BARS)
    test.print_musical_list()

    # 1. generate music usign my internal data structure
    # 2. make structure compatible for lillypond
    # 3.a save lilypond version as text string
    # 3.b p



    # test this commit
