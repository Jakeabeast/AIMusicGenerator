# take in raw data and grade it in several different fitness functions
def all_default_test(rawData):    
    totalTests = 4
    totalTestValue = note_rest_ratio(rawData)
    totalTestValue += note_length_ratio(rawData)
    totalTestValue += contiguous_melody_ratio(rawData)
    totalTestValue += interval_size_ratio(rawData)

    return totalTestValue / totalTests


def note_rest_ratio(rawData, targetRestDecimal = 0.2):
    # default to 20% rest amount and 80% note amount
    restCount = 0; 
    total = 0; 
    for element in rawData.get_notes(): 
        if element[0] == "rest": 
            restCount += 1 
        total += 1 

    inaccuracy = abs(targetRestDecimal - restCount / total) 

    return 1.0 - inaccuracy

def note_length_ratio(rawData, targetWholeNoteDecimal = 0.1, targetHalfNoteDecimal = 0.2, targetQuarterNoteDecimal = 0.7):
    # default to 70% quarter, 20% half, 10% whole
    wholeCount = 0
    halfCount = 0
    quarterCount = 0
    total = 0
    for element in rawData.get_notes():
        if element[2] == "whole":
            wholeCount += 1
        elif element[2] == "half":
            halfCount +=1
        elif element[2] == "quarter":
            quarterCount += 1
        else:
            return "ERROR UNKNOWN LENGTH"
        total += 1

    inaccuracy = abs(targetWholeNoteDecimal - wholeCount / total)
    inaccuracy += abs(targetHalfNoteDecimal - halfCount / total)
    inaccuracy += abs(targetQuarterNoteDecimal - quarterCount / total)

    return 1.0 - inaccuracy / 3 #average inaccuracy

def contiguous_melody_ratio(rawData, targetHarmonicDecimal = 0.8):
    #contiguous notes in sections of 3
    notesArray = rawData.get_notes()
    sectionIdx = 0
    harmonicSections = 0
    totalNotes = len(notesArray)
    while sectionIdx < totalNotes - 2:
        intervalJump12 = compare_note_interval(notesArray[sectionIdx][0], notesArray[sectionIdx + 1][0])
        intervalJump23 = compare_note_interval(notesArray[sectionIdx + 1][0], notesArray[sectionIdx + 2][0])

        if intervalJump12 == "rest" or intervalJump23 == "rest":
            pass
        #multiply jump, if both are positive or negative (going up or down), result is > 0, hence harmonic
        elif intervalJump12 * intervalJump23 > 0:
            harmonicSections +=1    

        sectionIdx += 1

    inaccuracy = abs(targetHarmonicDecimal - harmonicSections / totalNotes)

    return 1.0 - inaccuracy

def interval_size_ratio(rawData, targetIntervalDecimal = 0.5, scaleDegree = 2):
    #interval size default to 80% of scale degree 2 (2 intervals apart)
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
    inaccuracy = abs(targetIntervalDecimal - appropriateIntervals / totalIntervals)
    return 1.0 - inaccuracy

def compare_note_interval(note1, note2):
    #return positive if going up, negative if going down, rest if comparing note to a rest
    noteValuePair = {'c': 1, 'd': 2, 'e': 3, 'f': 4, 'g': 5, 'a': 6, 'b': 7}
    if note1 == "rest" or note2 == "rest":
        return "rest"
    else:
        return noteValuePair[note2] - noteValuePair[note1]