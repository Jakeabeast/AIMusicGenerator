from config import configFitness


# take in raw data and grade it in several different fitness functions
def all_default_tests(musicData):
	fitness = {
	"overall_score" : None,
	"note_rest_ratio": test_note_rest_ratio(musicData),
	"note_length_ratio" : test_contiguous_melody_shape_ratio(musicData),
	"contiguous_melody_ratio" : test_contiguous_melody_shape_ratio(musicData),
	"interval_size_ratio" : test_interval_size_ratio(musicData),
	"allowable_interval_size" : test_allowable_intervals(musicData),
	# "rhythm_complexity": test_rhythm_complexity(musicData),
	# "harmonic_consistency": test_harmonic_consistency(musicData) 
	}

	fitness["overall_score"] = sum(value for key, value in fitness.items() if key != "overall_score" ) / (len(fitness) - 1)

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

def test_allowable_intervals(musicData, soft_penalty=False):
    allowedIntervals = configFitness["interval_sizes_allowed"]
    notesArray = musicData["noteArray"]
    totalIntervals = 0
    acceptableIntervals = 0
    for noteIdx in range(len(notesArray) - 1):
        intervalJump = compare_note_interval(notesArray[noteIdx][0], notesArray[noteIdx + 1][0])
        if intervalJump != "rest":
            intervalJumpMag = abs(intervalJump)
            if intervalJumpMag in allowedIntervals:
                acceptableIntervals += 1
            elif soft_penalty:
                acceptableIntervals += 0.5  # Less harsh penalty for close intervals
            totalIntervals += 1
 
    if totalIntervals > 0:
        return 1.0 - (totalIntervals - acceptableIntervals) / totalIntervals
    else:
        return 0


def test_interval_size_ratio(musicData, tolerance=0.05):
    #interval size default to: size0 - 30%, size1 - 50%, size2 - 20%
    intervalPercent = {0: [configFitness["interval_size_ratio"][0], 0],
                       1: [configFitness["interval_size_ratio"][1], 0],
                       2: [configFitness["interval_size_ratio"][2], 0]}
 
    notesArray = musicData["noteArray"]
    totalIntervals = 0
    for noteIdx in range(len(notesArray) - 1):
        intervalJump = compare_note_interval(notesArray[noteIdx][0], notesArray[noteIdx + 1][0])
        if intervalJump != "rest":
            intervalJumpMag = abs(intervalJump)
            if intervalJumpMag <= 2:  # Only considering interval sizes 0, 1, 2
                intervalPercent[intervalJumpMag][1] += 1 
            totalIntervals += 1
 
    if totalIntervals > 0:
        accumInaccuracy = 0
        for i in range(3):
            target = intervalPercent[i][0]
            actual = intervalPercent[i][1] / totalIntervals
            # Apply tolerance so small deviations aren't penalized too harshly
            if abs(target - actual) > tolerance:
                accumInaccuracy += abs(target - actual)
        return 1.0 - accumInaccuracy / 3  # Return fitness score
    else:
        return 0

def compare_note_interval(note1, note2):
	#return positive if going up, negative if going down, rest if comparing note to a rest
	noteValuePair = {'c': 1, 'd': 2, 'e': 3, 'f': 4, 'g': 5, 'a': 6, 'b': 7, 'C' : 8}
	if note1 == "rest" or note2 == "rest":
		return "rest"
	else:
		return noteValuePair[note2] - noteValuePair[note1]
	
#reward simpler rhythms (grade 1  style)
# def test_rhythm_complexity(musicData):
#     note_lengths = [note[1] for note in musicData['noteArray'] if note[0] != 'rest']
#     unique_lengths = len(set(note_lengths))
#     total_notes = len(note_lengths)
#     return unique_lengths / total_notes if total_notes > 0 else 0

#reward harmonic intervals (***)
# def test_harmonic_consistency(musicData):
#     notes = musicData["noteArray"]
#     harmony_score = 0
#     for i in range(1, len(notes)):
#         if notes[i][0] != "rest" and notes[i-1][0] != "rest":
#             interval = abs(compare_note_interval(notes[i][0], notes[i-1][0]))
#             if interval in [0, 3, 4, 5, 7]:  # Harmonic intervals
#                 harmony_score += 1
#     return harmony_score / len(notes) if len(notes) > 0 else 0