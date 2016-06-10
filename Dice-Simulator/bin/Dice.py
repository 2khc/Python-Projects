import random


class Dice(object):
    def __init__(self, numOfFaces):
        self.num_of_faces = numOfFaces

    def roll(self):
        return random.randrange(1, self.num_of_faces, 1)

    def change_sides(self, num_of_faces):
        self.num_of_faces = num_of_faces
