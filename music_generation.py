import random
from fitness import all_default_tests

class UnrefinedMusicPiece:
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
		remainingBeatsInBar = self.timeSig[1]
		barCount = 1
		prevNotePitch = None

		weightingGuide = { 	'a' : [3, 4, 2, 1, 1, 2, 4],
							'b' : [4, 3, 4, 2, 1, 1, 2],
							'c' : [2, 4, 3, 4, 2, 1, 1],
							'C' : [2, 4, 3, 4, 2, 1, 1],
							'd' : [1, 2, 4, 3, 4, 2, 1],
							'e' : [1, 1, 2, 4, 3, 4, 2],
							'f' : [2, 1, 1, 2, 4, 3, 4],
							'g' : [4, 2, 1, 1, 2, 4, 3],
							None: [1, 1, 1, 1, 1, 1, 1] }

		random.seed(self.seed)
		while remainingSong > 0:
			element = random.choices(("note", "rest"), weights=None)[0] #weighting on initial population helps gives direction

			if element == "rest" and remainingBeatsInBar >= 1:
				note = "rest"
				prevNotePitch = None
				accidental = ""
				duration = ["crotchet", 1] #only quarter rests for now


			else:
				note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g'], weights = None)[0]
				#assumes keysig is C, applies c as octave high and low depending on previous note
				if self.keySig[0] == "C" and note == "c":
					if prevNotePitch in('g', 'a', 'b', 'C'): note = "C" 
					else: note = "c"

				prevNotePitch = note
				accidental = "natural" #add different accidentals later
					
				if remainingBeatsInBar >= 4:
					duration = random.choices((["semibreve",4],["dottedMinim",3],["minim",2],["crotchet",1],["quaver",0.5]), weights=None)[0]
				elif remainingBeatsInBar >= 3:
					duration = random.choices((["dottedMinim",3],["minim",2],["crotchet",1],["quaver",0.5]), weights=None)[0]
				elif remainingBeatsInBar >= 2:
					duration = random.choices((["minim",2],["crotchet",1],["quaver",0.5]), weights=None)[0]
				elif remainingBeatsInBar >= 1:
					duration = random.choices((["crotchet",1],["quaver",0.5]), weights=None)[0]
				else:
					duration = ["quaver", 0.5]
					
			musicArray.append([note, accidental, duration[0], barCount])

			remainingSong -= duration[1]
			remainingBeatsInBar -= duration[1]
			if remainingBeatsInBar <= 0:
				remainingBeatsInBar = self.timeSig[1]
				barCount += 1

		#print(musicArray) #shows data strcuture of music piece 
		return musicArray

def generate_initial_population(config):
	sample = []
	for _ in range(config["populationSize"]):
		tmpObj = UnrefinedMusicPiece(bars = config["numberBars"])
		tmpMusicDict = {"bars" : config["numberBars"],
						"keySig" : tmpObj.keySig,
						"clef" : tmpObj.clef,
						"timeSig" : [4, 4],
						"noteArray": tmpObj.noteArray}
		
		tmpFitnessDict = all_default_tests(tmpMusicDict)
		sample.append([tmpMusicDict, tmpFitnessDict])
	return sample