from config import active_config as config


# take in raw data and grade it in several different fitness functions
def all_default_test(rawData):    
	try:
		accumTestValue = 0
		numTests = 0
		for name, fitnessTest in globals().items():
			if name.startswith('test_') and callable(fitnessTest):
				testScore = fitnessTest(rawData)
				accumTestValue += testScore
				numTests += 1
		
		overallScore = accumTestValue / numTests

	except Exception as e:
		assert(e)

	return overallScore


def test_note_rest_ratio(rawData):
	# default to 10% rest amount and 90% note amount
	targetRestDecimal = 0.10 if config is None else config.note_rest_ratio

	restCount = 0; 
	totalBeats = rawData.numberOfBars * rawData.timeSig[1]; 
	for element in rawData.noteArray: 
		if element[0] == "rest": 
			restCount += 1 

	inaccuracy = abs(targetRestDecimal - restCount / totalBeats) 
	scaledInaccuracy = inaccuracy * 2

	return 1.0 - scaledInaccuracy

def test_note_length_ratio(rawData):
	# default to 85% crotchet, 10% quaver, 5% other
	if config is None:
		targetCrotchetNoteDecimal = 0.85
		targetQuaverNoteDecimal = 0.10
		targetOtherNoteDecimal = 0.05
	else:
		targetCrotchetNoteDecimal = config.note_length_ratio[0]
		targetQuaverNoteDecimal = config.note_length_ratio[1]
		targetOtherNoteDecimal = config.note_length_ratio[2]

	semibreveBeats = 0
	dottedMinimBeats = 0
	minimBeats = 0
	crotchetBeats = 0
	quaverBeats = 0
	totalBeats = 0
	for element in rawData.noteArray:
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

def test_contiguous_melody_shape_ratio(rawData):
	#default is 30% of sections is harmonic while 70% are not
	#note: assumes harmonic section to be contiguous notes in section of (default 3) to be ascending or descending 
	if config is None:
		targetHarmonicDecimal = 0.3
	else:
		targetHarmonicDecimal = config.contiguous_melody_ratio[0]

	notesArray = rawData.noteArray
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

def test_allowable_intervals(rawData):
	if config is None:
		allowedIntervals = [0, 1, 2]
	else:
		allowedIntervals = config.interval_sizes_allowed
		
	notesArray = rawData.noteArray
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


def test_interval_size_ratio(rawData):
	#interval size default to: size0 - 30%, size1 - 50%, size2 - 20% | where size is pitch jump distance from one note to the next
	intervalPercent = {}
	if config is None:
		intervalPercent[0] = [0.3, 0]
		intervalPercent[1] = [0.5, 0]
		intervalPercent[2] = [0.2, 0]
	else:
		intervalPercent[0] = [config.interval_size_ratio[0], 0]
		intervalPercent[1] = [config.interval_size_ratio[1], 0]
		intervalPercent[2] = [config.interval_size_ratio[2], 0]

	notesArray = rawData.noteArray
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
	
