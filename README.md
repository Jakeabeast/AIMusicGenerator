# Music Generator Project

## Purpose

To synthesize sight-reading exercises for beginner musicians using machine learning
By the end of this project, we will aim to deploy using a web-based interface.

## Where Abouts Are We?

So far the application is capable of producing textfiles of randomized exercises given a set amount of bars. Other musical characteristics can be customized to produce different keys and time signatures through overloaded methods.

The text files can be used by an application called Lilypond to display it's corresponding musical representation on a GUI
Lilypond - A music engraving program that takes in a file and converts it to display sheet music.

Additionally, a base fitness test has been implemented that is capable of ranking exercises based of suggestive data. These test include attributes such as amount of rests in a piece, note length ratio, melody raio, and ideal interval jumps.
The purpose of this fitness test is to provide an overall ranking of quality, however at this stage this is only based off suggestive data.

Lastly, exercises are seeded to analyse specific examples and compare.

## Whats Next?

The next steps is to incorporate an evolutionary algorithm that can reiterate through exercises and produce better quality piece according to a well defined fitness test. 

From here, we can deploy the application online and evaluate it's impact on beginner musicians.
Given time, we could further extend the application by introducing new musical characteristics for high level musicians.

## Dictionary of Files
main.py
- Runs the overview diagram shown in Research article page 2 figure 1 

config.py
- Fitness config: manually set targets for our fitness tests (explanation in file)
- Genetic config: manually set variables relating to the algorthim (explanation in file)

evolutionary_functions.py
- Pareto selection: Selecting 2 "superior" parents from a population ("superior" refers to music where all individual fitness aspects (not the overall fitness) are equal or greater than the other candadites within the population)
- Uniform crossover: Takes 2 parents (ideally selected using Pareto) and mixes genes to create 2 children. (Each bar within a piece of music has a chance to go to child 1 or 2, creating a uniform distribution)
- Mutation: Takes a child and applies a random mutation from the mutation functions below

fitness.py
- takes a piece of music and evaluates the fitness based off the imported fitness configuration dictionary (from config.py)
- maximum score for each fitness test is 1.0
- 'all_default_tests' gets the averaged score of all 5 individual fitness tests

graph.py
- (NOTE: not currently used due to multiple generations being produced which overwhelms the code)
- graphs the results of populations fitness (traffic lights implemented)

music_conversion.py
- translates the raw music data into a string that Lilypond (textgrave music editor software) can interpret properly

music_file.py
- (NOTE: not currently used, needs redesign to fit new data structure system implemented to manage populations)
- creates a text file for Lilypond to intepret multiple music pieces with the fitness values commented on.

music_generation.py
- creates randomized (though weighted to guide initial population) music, specifically for the first population


