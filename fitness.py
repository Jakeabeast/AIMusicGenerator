# take in raw data and grade it in several different fitness functions
def all_default_test(rawData):    

    # Ensure weighting adds to 1 (e.g 0.4 + 0.2 + 0.1 + 0.2 = 1)
    try:
        totalTestValue = note_rest_ratio(rawData) * 0.4
        totalTestValue += note_length_ratio(rawData) * 0.2
        totalTestValue += contiguous_melody_ratio(rawData) * 0.1
        totalTestValue += interval_size_ratio(rawData) * 0.2
    except Exception as e:
        print(e)
        return -1

    return totalTestValue


def note_rest_ratio(rawData, targetRestDecimal = 0.15):
    # default to 15% rest amount and 85% note amount
    restCount = 0; 
    totalBeats = rawData.get_numberOfBars() * rawData.get_timeSignature()[1]; 
    for element in rawData.get_notes(): 
        if element[0] == "rest": 
            restCount += 1 

    inaccuracy = abs(targetRestDecimal - restCount / totalBeats) 
    scaledInaccuracy = inaccuracy * 2

    return 1.0 - scaledInaccuracy

def note_length_ratio(rawData, targetWholeNoteDecimal = 0.1, targetHalfNoteDecimal = 0.2, targetQuarterNoteDecimal = 0.7):
    # default to 70% quarter, 20% half, 10% whole
    wholeCount = 0
    halfCount = 0
    quarterCount = 0
    totalBeats = 0
    for element in rawData.get_notes():
        if element[2] == "whole":
            wholeCount += 4
            totalBeats += 4
        elif element[2] == "half":
            halfCount +=2
            totalBeats += 2
        elif element[2] == "quarter":
            quarterCount += 1
            totalBeats += 1
        else:
            return "ERROR UNKNOWN LENGTH"


    inaccuracy = abs(targetWholeNoteDecimal - wholeCount / totalBeats) 
    inaccuracy += abs(targetHalfNoteDecimal - halfCount / totalBeats) 
    inaccuracy += abs(targetQuarterNoteDecimal - quarterCount / totalBeats) 
    scaledInaccuracy = inaccuracy * 0.5

    return 1.0 - scaledInaccuracy

def contiguous_melody_ratio(rawData, targetHarmonicDecimal = 0.8):
    #contiguous notes in sections of 3
    notesArray = rawData.get_notes()
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

def testcontiguous_melody_ratio(rawData, targetHarmonicDecimal = 0.8):
    #contiguous notes in sections of 3
    notesArray = rawData.get_notes()
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

def interval_size_ratio(rawData, targetIntervalDecimal = 0.5, scaleDegree = 2):
    #interval size default to 50% of scale degree 2 (2 intervals apart)
    notesArray = rawData.get_notes()
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
        return "0 Intervals"
    
    return 1.0 - inaccuracy

def compare_note_interval(note1, note2):
    #return positive if going up, negative if going down, rest if comparing note to a rest
    noteValuePair = {'c': 1, 'd': 2, 'e': 3, 'f': 4, 'g': 5, 'a': 6, 'b': 7}
    if note1 == "rest" or note2 == "rest":
        return "rest"
    else:
        return noteValuePair[note2] - noteValuePair[note1]