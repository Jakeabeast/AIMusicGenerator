
"""
Musical Characteristics/Attributes
----------
note_rest_ratio : int 
	decimal percentage of rests to notes (e.g 0.15 indicates 15% rest to 85% notes)
note_length_ratio: list[3]
	percentage distribution of the note lengths (e.g [0.7, 0.2, 0.1] indicate 70% crotchet - 20% quaver - 10% other)
contiguous_melody_ratio : list[2]
	percentage of harmonic sections (e.g [0.5] indicates 50% of harmonic sections of length 3) [3 is default]
interval_size_ratio : list[2]
	percentage of appropriate interval size (e.g [0.2, 0.5, 0.3] indicates 20% pitch is same size, 50% is one size apart, 30% is of two size apart
interval_sizes_allowed : list[any]
	what intervals sizes are allowed (e.g [0, 1, 2] indicates pitch jumps of 0 - 2 are allowed)
"""
configFitness = {
	"note_rest_ratio" : 0.1, 
	"note_length_ratio" : [0.85, 0.10, 0.05],
	"contiguous_melody_shape_ratio" : 0.3,
	"interval_sizes_allowed" : [0, 1, 2], 
	"interval_size_ratio" : [0.3, 0.5, 0.2]
}


"""
Genetic Algorithm Parameters
----------
numberBars : int
	how many bars in a piece of music
populationSize : int
	how big is a population sample before regenerating a new population
mutationChance : int
	percentage chance of a child to be mutated 
terminationNumber : int
	how many times population is recreated without any improvement to best candidate
"""
configGenetic = {
	"numberBars" : 16,
    "numberElites" : 1,
	"populationSize" : 50,
	"mutationChance" : 1,
	"terminationNumber" : 10
}