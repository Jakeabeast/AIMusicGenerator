import random

class UnrefinedMusic:
    #overloaded constructors
    def __init__ (self, bars):
        self.numberOfBars = bars
        self.keySig = ["C", "major"] #Cmajor
        self.clef = "treble" #Treble Clef
        self.timeSig = [4,4] #Common time

    def __init__ (self, bars, keySignature):
        self.numberOfBars = bars
        self.keySig  = keySignature # "C", "major/minor" = Cmajor / Cminor
        self.clef = "treble" #Treble Clef
        self.timeSig = [4,4] #Common time

    def __init__ (self, bars, keySignature, clef):
        self.numberOfBars = bars
        self.keySig  = keySignature # "C", "major/minor" = Cmajor / Cminor
        self.clef = clef # "treble" / "bass"
        self.timeSig = [4,4] #Common time

    def __init__ (self, bars, keySignature, clef, timeSignature):
        self.numberOfBars = bars
        self.keySig = keySignature # "C", "major/minor" = Cmajor / Cminor
        self.clef = clef # "treble" / "bass"
        self.timeSig = timeSignature # [beats per bar, value per beat]

    #accessors
    def get_numberOfBars(self):
        return self.numberOfBars    

    def get_keySignature(self):
        return self.keySig
    
    def get_clef(self):
        return self.clef

    def get_timeSignature(self):
        return self.timeSig

    #methods
    def raw_music(self):
        musicArray = []
        remainingSong = self.numberOfBars * self.timeSig[1] 

        while remainingSong > 0:
            note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
            note = note[0]
            accidental = "natural" #add different accidentals later
            
            while True:
                duration = random.choices((["whole",4],["half",2],["quarter",1]), weights=(14,28,58))
                duration = duration[0]
                if duration[1] <= remainingSong: break

            remainingSong -= duration[1]            
            musicArray.append([note, accidental, duration[0]])

        return musicArray
    

class RawLilypond:
    #contructor
    def __init__(self, rawData):
        self.numberOfBars = rawData.get_numberOfBars()
        self.timeSig = rawData.get_timeSignature()
        self.clef = rawData.get_clef()
        self.keySig = rawData.get_keySignature()

        self.refinedMusic = self.refine_music(rawData)

    #accessors
    def get_refinedMusic(self):
        return self.refinedMusic

    #methods
    def refine_music(self, rawData):
        remainingBeatsInBar = self.timeSig[1]
        raw_data_array = rawData.raw_music()
        refined_notes_array = []

        for i in range(len(raw_data_array)):
            note = raw_data_array[i][0]
            accidental = self.convert_accidental(raw_data_array[i][1])
            duration = self.convert_duration(raw_data_array[i][2])

            if duration > remainingBeatsInBar:
                refined_notes_array.append([note, accidental, remainingBeatsInBar, "~"])
                refined_notes_array.append([note, accidental, duration-remainingBeatsInBar, ""])
                remainingBeatsInBar = self.timeSig[1] - (duration - remainingBeatsInBar)
            else:
                refined_notes_array.append([note, accidental, duration, ""])
                remainingBeatsInBar -= duration
                if remainingBeatsInBar <= 0:
                    remainingBeatsInBar = self.timeSig[1]

        return [self.timeSig, self.clef, self.keySig, refined_notes_array]

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
        
    def convert_accidental(self, accidental):
        if accidental == "natural":
            return ""
        elif accidental == "sharp":
            return "is"
        elif accidental == "flat":
            return "es"
        else:
            return -1 
        
class EngravedLilypond:
    #constructor 
    def __init__(self, rawLilypond):
        print(self.text_file(rawLilypond.get_refinedMusic()))

    def text_file(self, rawLilypond):
        text = "{ "
        text += "\\time " + str(rawLilypond[0][0]) + "/" + str(rawLilypond[0][1]) + " "
        text += "\\clef " + rawLilypond[1].lower() + " "
        text += "\\key " + rawLilypond[2][0].lower() + " \\" + rawLilypond[2][1].lower() + " "
    
        for i in range(len(rawLilypond[3])):
            text += self.format_note(rawLilypond[3][i])

        text += "}"
        return text
    
    def format_note(self, noteArray):
        noteText = noteArray[0] #note
        noteText += noteArray[1] #accident
        noteText += "\'" #octaveRange (non-changable)
        noteText += self.convert_duration(noteArray[2]) #duration
        noteText += noteArray[3]
        noteText += " "

        return noteText
    
    def convert_duration(self, duration):
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
    

    # 1. generate music usign my internal data structure
    # 2. make structure compatible for lillypond
    # 3.a save lilypond version as text string