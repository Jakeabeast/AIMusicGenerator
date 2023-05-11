import random

class UnrefinedMusic:
    #overloaded constructors
    def __init__ (self, seed = random.random(), bars = 8, keySignature = ["C", "major"], clef = "treble", timeSignature = [4,4]):

        self.seed = seed
        self.numberOfBars = bars
        self.keySig = keySignature # "C", "major/minor" = Cmajor / Cminor
        self.clef = clef # "treble" / "bass"
        self.timeSig = timeSignature # [beats per bar, value per beat]

        self.noteArray = self.raw_music()

    #accessors
    def get_numberOfBars(self):
        return self.numberOfBars

    def get_keySignature(self):
        return self.keySig
    
    def get_clef(self):
        return self.clef

    def get_timeSignature(self):
        return self.timeSig
    
    def get_notes(self):
        return self.noteArray
    
    def get_seed(self):
        return self.seed
    
    def set_seed(self, seed):
        self.seed = seed
        self.noteArray = self.raw_music()

    #methods
    def raw_music(self):
        musicArray = []
        remainingSong = self.numberOfBars * self.timeSig[1] #4 bars in common time makes 4 * 4 = 16 beats

        random.seed(self.seed)
        while remainingSong > 0:
            element = random.choices(("note", "rest"), weights=(80,20))
            element = element[0]

            if (element == "rest"):
                note = "rest"
                accidental = ""
                duration = ["quarter", 1] #only quarter rests for now

            elif (element == "note"):
                note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
                note = note[0]
                accidental = "natural" #add different accidentals later
                    
                while True:
                    duration = random.choices((["whole",4],["half",2],["quarter",1]), weights=None) 
                    duration = duration[0]
                    if duration[1] <= remainingSong: 
                        break

            remainingSong -= duration[1]
            musicArray.append([note, accidental, duration[0]])

        return musicArray
    

class Lilypond:
    #contructor
    def __init__(self, rawData, fileName = "test"):
        self.numberOfBars = rawData.get_numberOfBars()
        self.timeSig = rawData.get_timeSignature()
        self.clef = rawData.get_clef()
        self.keySig = rawData.get_keySignature()
        self.refinedNotes = self.refine_music_notes(rawData)

        self.text_file(fileName)

    #accessors
    def get_refinedMusic(self):
        return self.refinedNotes

    #methods     
    def refine_music_notes(self, rawData):
        remainingBeatsInBar = self.timeSig[1]
        raw_data_array = rawData.get_notes()
        refined_notes_array = []

        for i in range(len(raw_data_array)):
            note = self.convert_note(raw_data_array[i][0])
            accidental = self.convert_accidental(raw_data_array[i][1])
            duration = self.convert_duration(raw_data_array[i][2])

            if duration > remainingBeatsInBar:
                refined_notes_array.append([note, accidental, self.convert_beat(remainingBeatsInBar), "~"])
                refined_notes_array.append([note, accidental, self.convert_beat(duration-remainingBeatsInBar), ""])
                remainingBeatsInBar = self.timeSig[1] - (duration - remainingBeatsInBar)
            else:
                refined_notes_array.append([note, accidental, self.convert_beat(duration), ""])
                remainingBeatsInBar -= duration
                if remainingBeatsInBar <= 0:
                    remainingBeatsInBar = self.timeSig[1]

        return refined_notes_array

    def convert_note(self, note):
        if note == "rest":
            return 'r'
        else:
            return note

    def convert_accidental(self, accidental):
        if accidental == "natural" or accidental == "":
            return ""
        elif accidental == "sharp":
            return "is"
        elif accidental == "flat":
            return "es"
        else:
            return -1 

    def convert_duration(self, duration):
        if duration == "whole":
            return 4
        elif duration == 3:
            return 3
        elif duration == "half" or duration == 2:
            return 2
        elif duration == "quarter" or duration == 1:
            return 1
        else:
            return -1 
        
    def convert_beat(self, duration):
        if duration == 4:
            return "1"
        elif duration == 3:
            return "2." #funny special dotted note thingy
        elif duration == 2:
            return "2"
        elif duration == 1:
            return "4"
        else:
            return "ERROR, REPORT ME" 
        
    def text_file(self, fileName):
        text = "{ "
        text += "\\time " + str(self.timeSig[0]) + "/" + str(self.timeSig[1]) + " "
        text += "\\clef " + self.clef.lower() + " "
        text += "\\key " + self.keySig[0].lower() + " \\" + self.keySig[1].lower() + " "
    
        for i in range(len(self.refinedNotes)):
            text += self.format_notes(self.refinedNotes[i])

        text += "}\n"
        
        file = open(fileName + "File.txt", 'a')
        file.write(text)
        file.close()

        print(text) #comment out to stop showing in terminal

    def format_notes(self, noteArray):
        noteText = noteArray[0] #note
        noteText += noteArray[1] #accident
        if noteArray[0] != 'r': noteText += "\'" #octaveRange for notes(non-changable)
        noteText += noteArray[2] #duration
        noteText += noteArray[3]
        noteText += " "

        return noteText