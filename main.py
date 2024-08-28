import music
import fitness
import music_file
import config
import graph



#print out data of single piece given a seed (e.g 'test_seed(0.539230033491368)')
def test_seed(seed):
	rawData = music.UnrefinedMusic(seed = seed)
	music.Lilypond(rawData)
	print("Fitness Test (Note:Rest)= {0}\n".format(fitness.note_rest_ratio(rawData)))
	print("Fitness Test (Note Length)= {0}\n".format(fitness.note_length_ratio(rawData)))
	print("Fitness Test (Melody)= {0}\n".format(fitness.contiguous_melody_ratio(rawData)))
	print("Fitness Test (Melody Test) [Allow same pitch x2]= {0}\n".format(fitness.testcontiguous_melody_ratio(rawData)))
	print("Fitness Test (Interval Size)= {0}\n".format(fitness.interval_size_ratio(rawData)))
	print("Fitness Test (Overall)= {0}\n\n\n".format(fitness.all_default_test(rawData)))



if __name__ == "__main__":
	config.configV1.print_config()
	#config.active_config = config.configV1
	music_file.create_file(numMusic = 1000, numBars = 8)
	
	#draw graph of created file
	graph.draw()


	music_file.sort_by_rank("NoteToRest")
	music_file.sort_by_rank("NoteLength")
	music_file.sort_by_rank("Melody")
	music_file.sort_by_rank("IntervalSize")
	music_file.sort_by_rank("Overall")	
