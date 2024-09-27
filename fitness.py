from config import configFitness


# take in raw data and grade it in several different fitness functions
def all_default_tests(musicData):
	fitness = {
	"overall_score" : None,
	"note_rest_ratio": None,
	"note_length_ratio" : None,
	"contiguous_melody_ratio" : None,
	"interval_size_ratio" : None,
	"allowable_interval_size" : None
	}

	fitness["note_rest_ratio"] = test_note_rest_ratio(musicData)
	fitness["note_length_ratio"] = test_note_length_ratio(musicData)
	fitness["contiguous_melody_ratio"] = test_contiguous_melody_shape_ratio(musicData)
	fitness["interval_size_ratio"] = test_allowable_intervals(musicData)
	fitness["allowable_interval_size"] = test_interval_size_ratio(musicData)

	fitness["overall_score"] = (fitness["note_rest_ratio"] + fitness["note_length_ratio"] + fitness["contiguous_melody_ratio"] \
							 + fitness["interval_size_ratio"] + fitness["allowable_interval_size"]) / 5

	return fitness


def test_note_rest_ratio(musicData):
	targetRestDecimal = configFitness["note_rest_ratio"]

	restCount = 0; 
	totalBeats = musicData["bars"] * musicData["timeSig"][1]; 
	for element in musicData["noteArray"]: 
		if element[0] == "rest": 
			restCount += 1 

	inaccuracy = abs(targetRestDecimal - restCount / totalBeats) 
	scaledInaccuracy = inaccuracy * 2

	return 1.0 - scaledInaccuracy

def test_note_length_ratio(musicData):
	targetCrotchetNoteDecimal = configFitness["note_length_ratio"][0]
	targetQuaverNoteDecimal = configFitness["note_length_ratio"][1]
	targetOtherNoteDecimal = configFitness["note_length_ratio"][2]

	semibreveBeats = 0
	dottedMinimBeats = 0
	minimBeats = 0
	crotchetBeats = 0
	quaverBeats = 0
	totalBeats = 0
	for element in musicData["noteArray"]:
		if element[2] == "semibreve":
			semibreveBeats += 4
			totalBeats += 4
		elif element[2] == "dottedMinim":
			dottedMinimBeats += 3
			totalBeats += 3
		elif element[2] == "minim":
			minimBeats += 2
			totalBeats += 2
		elif element[2] == "crotchet":
			crotchetBeats += 1
			totalBeats += 1
		elif element[2] == "quaver":
			quaverBeats += 0.5
			totalBeats += 0.5
		else:
			assert "ERROR UNKNOWN LENGTH"


	inaccuracy = abs(targetCrotchetNoteDecimal - crotchetBeats / totalBeats) 
	inaccuracy += abs(targetQuaverNoteDecimal - quaverBeats / totalBeats) 
	otherBeats = semibreveBeats + dottedMinimBeats + minimBeats
	inaccuracy += abs(targetOtherNoteDecimal - otherBeats / totalBeats) 

	return max(0, 1.0 - inaccuracy)

def test_contiguous_melody_shape_ratio(musicData):
	#note: assumes harmonic section to be contiguous notes in section of (default 3) to be ascending or descending 
	targetHarmonicDecimal = configFitness["contiguous_melody_shape_ratio"]

	notesArray = musicData["noteArray"]
	sectionIdx = 0
	harmonicSections = 0
	totalSections = 0
	totalNotes = len(notesArray)
	while sectionIdx < totalNotes - 2:
		# compare 3 notes together: return rest if a note is a rest | return negative number if going up | positive ig going down
		intervalJump12 = compare_note_interval(notesArray[sectionIdx][0], notesArray[sectionIdx + 1][0])
		intervalJump23 = compare_note_interval(notesArray[sectionIdx + 1][0], notesArray[sectionIdx + 2][0])

		if intervalJump12 == "rest" or intervalJump23 == "rest":
			pass
			totalSections -= 1
		#multiply jump, if both are positive or negative (going up or down), result is > 0, hence harmonic shape
		elif intervalJump12 * intervalJump23 > 0:
			harmonicSections +=1    

		totalSections += 1
		sectionIdx += 1
	try:
		inaccuracy = abs(targetHarmonicDecimal - harmonicSections / totalSections)
	except: 
		return 0
	
	return 1.0 - inaccuracy

def test_allowable_intervals(musicData):
	allowedIntervals =  configFitness["interval_sizes_allowed"]
		
	notesArray = musicData["noteArray"]
	noteIdx = 0
	totalIntervals = 0
	acceptableIntervals = 0
	totalNotes = len(notesArray)
	while noteIdx < totalNotes - 1:
		intervalJump = compare_note_interval(notesArray[noteIdx][0], notesArray[noteIdx + 1][0])

		if intervalJump != "rest":
			intervalJumpMag = abs(intervalJump)
			if intervalJumpMag in allowedIntervals: acceptableIntervals += 1
			totalIntervals += 1
		noteIdx += 1

	if totalIntervals > 0:
		return 1.0 - acceptableIntervals / totalIntervals
	else:
		return 0


def test_interval_size_ratio(musicData):
	#interval size default to: size0 - 30%, size1 - 50%, size2 - 20% | where size is pitch jump distance from one note to the next
	intervalPercent = {}
	intervalPercent[0] = [configFitness["interval_size_ratio"][0], 0]
	intervalPercent[1] = [configFitness["interval_size_ratio"][1], 0]
	intervalPercent[2] = [configFitness["interval_size_ratio"][2], 0]


	notesArray = musicData["noteArray"]
	noteIdx = 0
	totalIntervals = 0
	totalNotes = len(notesArray)
	while noteIdx < totalNotes - 1:
		intervalJump = compare_note_interval(notesArray[noteIdx][0], notesArray[noteIdx + 1][0])

		if intervalJump != "rest":
			intervalJumpMag = abs(intervalJump)
			if intervalJumpMag <= 2: intervalPercent[intervalJumpMag][1] += 1 
			totalIntervals += 1
		noteIdx += 1

	accumInaccuracy = 0
	if totalIntervals > 0:
		#fitness = ALL (abs(targetPercent(size#) - number(size#)/total))
		accumInaccuracy += abs(intervalPercent[0][0] - intervalPercent[0][1] / totalIntervals)
		accumInaccuracy += abs(intervalPercent[1][0] - intervalPercent[1][1] / totalIntervals)
		accumInaccuracy += abs(intervalPercent[2][0] - intervalPercent[2][1] / totalIntervals)
		return 1.0 - accumInaccuracy / 3 #3 sizes tested

	else:
		return 0

def compare_note_interval(note1, note2):
	#return positive if going up, negative if going down, rest if comparing note to a rest
	noteValuePair = {'c': 1, 'd': 2, 'e': 3, 'f': 4, 'g': 5, 'a': 6, 'b': 7}
	if note1 == "rest" or note2 == "rest":
		return "rest"
	else:
		return noteValuePair[note2] - noteValuePair[note1]
	
