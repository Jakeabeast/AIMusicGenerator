from config import active_config as config


# take in raw data and grade it in several different fitness functions
def all_default_test(rawData):    
	try:
		totalTestValue = 0
		numTests = 0
		for name, fitnessTest in globals().items():
			if name.startswith('test_') and callable(fitnessTest):
				testScore = fitnessTest(rawData)
				totalTestValue += testScore
				numTests += 1
		
		overallScore = totalTestValue / numTests

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

def test_contiguous_melody_ratio(rawData):
	#default is 80% of sections is harmonic while 20% are not
	#note: assumes harmonic section to be contiguous notes in section of (default 3) to be ascending or descending 
	if config is None:
		targetHarmonicDecimal = 0.8
		harmonicSectionLength = 3
	else:
		targetHarmonicDecimal = config.contiguous_melody_ratio[0]
		harmonicSectionLength = config.contiguous_melody_ratio[1]

	notesArray = rawData.noteArray
	sectionIdx = 0
	harmonicSections = 0
	totalSections = 0
	totalNotes = len(notesArray)
	while sectionIdx < totalNotes - 2:
		intervalJump12 = compare_note_interval(notesArray[sectionIdx][0], notesArray[sectionIdx + 1][0])
		intervalJump23 = compare_note_interval(notesArray[sectionIdx + 1][0], notesArray[sectionIdx + 2][0])

		if intervalJump12 == "rest" or intervalJump23 == "rest":
			pass
			totalSections -= 1
		#multiply jump, if both are positive or negative (going up or down), result is > 0, hence harmonic
		elif intervalJump12 * intervalJump23 > 0:
			harmonicSections +=1    

		totalSections += 1
		sectionIdx += 1
	try:
		inaccuracy = abs(targetHarmonicDecimal - harmonicSections / totalSections)
	except: 
		return 0
	
	return 1.0 - inaccuracy

def samepitches_contiguous_melody_ratio(rawData, targetHarmonicDecimal = 0.8):
	#contiguous notes in sections of 3
	notesArray = rawData.noteArray
	sectionIdx = 0
	harmonicSections = 0
	totalSections = 0
	totalNotes = len(notesArray)
	while sectionIdx < totalNotes - 2:
		intervalJump12 = compare_note_interval(notesArray[sectionIdx][0], notesArray[sectionIdx + 1][0])
		intervalJump23 = compare_note_interval(notesArray[sectionIdx + 1][0], notesArray[sectionIdx + 2][0])

		if intervalJump12 == "rest" or intervalJump23 == "rest":
			pass
			totalSections -= 1
		#multiply jump, if both are positive or negative (going up or down), result is > 0, hence harmonic
		elif intervalJump12 * intervalJump23 >= 0 and intervalJump12 + intervalJump23 != 0:
			harmonicSections +=1    

		totalSections += 1
		sectionIdx += 1
	try:
		inaccuracy = abs(targetHarmonicDecimal - harmonicSections / totalSections)
	except: 
		return "0 Sections"
	
	return 1.0 - inaccuracy

def test_interval_size_ratio(rawData):
	#interval size default to 50% of scale degree 2 (2 intervals apart)
	if config is None:
		targetIntervalDecimal = 0.5
		scaleDegree = 2
	else:
		targetIntervalDecimal = config.interval_size_ratio[0]
		scaleDegree = config.interval_size_ratio[1]

	notesArray = rawData.noteArray
	noteIdx = 0
	appropriateIntervals = 0
	totalIntervals = 0
	totalNotes = len(notesArray)
	while noteIdx < totalNotes - 2:
		intervalJump = compare_note_interval(notesArray[noteIdx][0], notesArray[noteIdx + 1][0])

		if intervalJump == "rest":
			pass
			totalIntervals -= 1
		elif abs(intervalJump) <= scaleDegree:
			appropriateIntervals += 1
		
		totalIntervals += 1
		noteIdx += 1

	try:
		inaccuracy = abs(targetIntervalDecimal - appropriateIntervals / totalIntervals)
	except: 
		return 0 #"0 Intervals"
	
	return 1.0 - inaccuracy

def compare_note_interval(note1, note2):
	#return positive if going up, negative if going down, rest if comparing note to a rest
	noteValuePair = {'c': 1, 'd': 2, 'e': 3, 'f': 4, 'g': 5, 'a': 6, 'b': 7}
	if note1 == "rest" or note2 == "rest":
		return "rest"
	else:
		return noteValuePair[note2] - noteValuePair[note1]