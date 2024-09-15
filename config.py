active_config = None

class Config:
	"""
	Add configuration for the different fitness parameters

	Musical Characteristics/Attributes
	----------
	note_rest_ratio : int 
		decimal percentage of rests to notes (e.g 0.15 indicates 15% rest to 85% notes)
	note_length_ratio: list[3]
		percentage distribution of the note lengths (e.g [0.7, 0.2, 0.1] indicate 70% quarter - 20% half - 10% whole notes)
	contiguous_melody_ratio : list[2]
		percentage of harmonic sections (e.g [0.8, 3] indicates 80% of harmonic sections of length 3) note-leave list[1] = 3 please.
	interval_size_ratio : list[2]
		percentage of appropriate interval size (e.g [0.5, 2] indicates 50% of interval jumps are 2 pitches or less apart)
	"""

	def __init__(self, c1:int = None , c2:list[3] = None, c3:list[2] = None, c4:list[2] = None):
		self.note_rest_ratio = c1 
		self.note_length_ratio = c2
		self.contiguous_melody_ratio = c3
		self.interval_size_ratio = c4
	
	def print_config(self):
		print("%s, %s, %s, %s" % (self.note_rest_ratio, self.note_length_ratio, self.contiguous_melody_ratio, self.interval_size_ratio))

	def __str__(self):
		return "%s, %s, %s, %s" % (self.note_rest_ratio, self.note_length_ratio, self.contiguous_melody_ratio, self.interval_size_ratio)



configV1 = Config(0.1, [0.9, 0.1, 0.05], [0.8, 3], [0.5, 2])


active_config = configV1
