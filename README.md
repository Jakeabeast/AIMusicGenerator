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
