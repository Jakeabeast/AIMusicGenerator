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

		random.seed(self.seed)
		while remainingSong > 0:
			element = random.choices(("note", "rest"), weights=(90,10))[0] #(90% - notes, 10% - rests)

			if (element == "rest"):
				note = "rest"
				accidental = ""
				duration = ["crotchet", 1] #only quarter rests for now


			elif (element == "note"):
				note = random.choices(['a', 'b', 'c', 'd', 'e', 'f', 'g'])[0]
				accidental = "natural" #add different accidentals later
					
				if remainingBeatsInBar >= 4:
					duration = random.choices((["semibreve",4],["dottedMinim",3],["minim",2],["crotchet",1],["quaver",0.5]), weights=(6,3,3,85,3))[0]
				elif remainingBeatsInBar >= 3:
					duration = random.choices((["dottedMinim",3],["minim",2],["crotchet",1],["quaver",0.5]), weights=(5,7,84,9))[0]
				elif remainingBeatsInBar >= 2:
					duration = random.choices((["minim",2],["crotchet",1],["quaver",0.5]), weights=(5,85,10))[0]
				elif remainingBeatsInBar >= 1:
					duration = random.choices((["crotchet",1],["quaver",0.5]), weights=(95,5))[0]
				else:
					duration = ["quaver", 0.5]
					
			musicArray.append([note, accidental, duration[0], barCount])

			remainingSong -= duration[1]
			remainingBeatsInBar -= duration[1]
			if remainingBeatsInBar <= 0:
				remainingBeatsInBar = self.timeSig[1]
				barCount += 1

		print(musicArray)
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