import random

musicNotes = ["a", "b", "c", "d", "e", "f", "g"]

print("{ ", end=" ")
for i in range(8):
    print(random.choice(musicNotes) + '\' ', end=" ")

print("} ", end=" ") 

