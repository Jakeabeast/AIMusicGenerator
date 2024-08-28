import random

class UnrefinedMusic:
	#overloaded constructors
	def __init__ (self, seed = None, bars = 8, keySignature = ["C", "major"], clef = "treble", timeSignature = [4,4]):

		#can't use random.random as default param as it is called only once at function creation (need differenting seeds)
		self.seed = random.random() if seed is None else seed
		self.numberOfBars = bars
		self.keySig = keySignature # "C", "major/minor" = Cmajor / Cminor
		self.clef = clef # "treble" / "bass"
		self.timeSig = timeSignature # [beats per bar, value per beat]
		self.noteArray = self.raw_music()
	
	#accessors
	def seed_str(self):
		return str(self.seed)

	#methods
	def raw_music(self):
		musicArray = []
		remainingSong = self.numberOfBars * self.timeSig[1] #4 bars in common time makes 4 * 4 = 16 beats

		random.seed(self.seed)
		while remainingSong > 0:
			element = random.choices(("note", "rest"), weights=(85,15))[0] #(80,20)

			if (element == "rest"):
				note = "rest"
				accidental = ""
				duration = ["quarter", 1] #only quarter rests for now

			elif (element == "note"):
				note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g'])[0]
				accidental = "natural" #add different accidentals later
					
				while True:
					duration = random.choices((["whole",4],["half",2],["quarter",1]), weights=None)[0]
					if duration[1] <= remainingSong: 
						break

			remainingSong -= duration[1]
			musicArray.append([note, accidental, duration[0]])

		return musicArray
	

class Lilypond:
	#contructor
	def __init__(self, rawData, file, fileName = "test"):
		self.numberOfBars = rawData.numberOfBars
		self.timeSig = rawData.timeSig
		self.clef = rawData.clef
		self.keySig = rawData.keySig
		self.refinedNotes = self.refine_music_notes(rawData)

		self.text_file(file, fileName)

	#accessors
	def get_refinedMusic(self):
		return self.refinedNotes

	#methods     
	def refine_music_notes(self, rawData):
		remainingBeatsInBar = self.timeSig[1]
		raw_data_array = rawData.noteArray
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
		
	def text_file(self, file, fileName):
		text = "{ "
		text += "\\time " + str(self.timeSig[0]) + "/" + str(self.timeSig[1]) + " "
		text += "\\clef " + self.clef.lower() + " "
		text += "\\key " + self.keySig[0].lower() + " \\" + self.keySig[1].lower() + " "
	
		for i in range(len(self.refinedNotes)):
			text += self.format_notes(self.refinedNotes[i])

		text += "}\n"
		from music_file import FILE_TYPE
		file.write(text)

		#print(text) #comment out to stop showing in terminal

	def format_notes(self, noteArray):
		noteText = noteArray[0] #note
		noteText += noteArray[1] #accident
		if noteArray[0] != 'r': noteText += "\'" #octaveRange for notes(non-changable)
		noteText += noteArray[2] #duration
		noteText += noteArray[3]
		noteText += " "

		return noteText