import numpy as np
import rotations

class Turtle:
    def __init__(self, initialCell):
        self.position   = np.array([0, 0, 0])
        self.heading    = np.eye(3)
        self.thickness  = 50.0
        self.crntCell   = initialCell

        self.heading = rotations.do_rot(self.heading, 1, 90)
        self.heading = rotations.do_rot(self.heading, 2, 90)

        self.parentHeading = self.heading[:,0]

    def Forward(self, length):
        self.position = self.position + length*self.heading[:,0]

    def Roll(self, axis_label, theta):
        self.heading = rotations.do_rot(self.heading, axis_label, theta)

    def View(self, includeAngles=False):
        pos = self.position
        if includeAngles==True:
            parentAngle = rotations.angleBetween(self.parentHeading, self.heading[:,0])
            verticalAngle = rotations.angleBetween([0,1,0], self.heading[:,0])
            horizontalAngle = rotations.angleBetween([1,0,0], self.heading[:,0])
            return (pos[0], pos[1], pos[2], self.thickness, verticalAngle, horizontalAngle, parentAngle)
        return (pos[0], pos[1], pos[2], self.thickness)

    def New(self):
        new = Turtle(self.crntCell)
        new.position = self.position
        new.heading  = self.heading
        new.thickness = self.thickness
        new.parentHeading = self.parentHeading
        return new

    def Decay(self):
        self.thickness *= self.crntCell.decay

    def Interpret(self, symbol):
        if symbol == "+":
            theta = self.crntCell.ValueOf("+")
            self.Roll(0, theta)
        elif symbol == "-":
            theta = self.crntCell.ValueOf("+")
            self.Roll(0, -theta)
        elif symbol == "n":
            theta = self.crntCell.ValueOf("n")
            self.Roll(1, theta)
        elif symbol == "u":
            theta = self.crntCell.ValueOf("u")
            self.Roll(1, -theta)
        elif symbol == ">":
            theta = self.crntCell.ValueOf(">")
            self.Roll(2, theta)
        elif symbol == "<":
            theta = self.crntCell.ValueOf("<")
            self.Roll(2, -theta)
        elif symbol == "D":
            decay = self.crntCell.ValueOf("D")
            self.thickness *= decay
        else:
            raise Exception("Turtle Interpretation Error: Symbol not found")
