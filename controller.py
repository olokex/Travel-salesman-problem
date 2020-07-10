#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from model import Model
from view import View
from constants import *
from utils import *
from exceptions import *


class Controller():
    """Main class that controlls all the events.
    If you want to test the code you should run this file."""


    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.timer = TIMER
        self.iterationCounter = 0
        """Distance has to start with a high number,
        because even the first one can be the shortest."""
        self.bestDistance = float("inf")
        """Check for user's input."""
        self.validInput = False
        self.bestPath = []


    def main(self):
        self.view.main()


    def start(self):
        if self.view.running == True:
            return
        self._getUserInputs()
        if self.validInput == False:
            return
        self.view.running = True
        self.view.drawCities(self.model.coordinates)
        self.view.connectCities(self.model.coordinates)
        self.view.setTimer(self.timer)


    def _getUserInputs(self):
        """Validates user's input
        for futher info read constants.py and model.
        """
        try:
            userCoor = self.view.textCoordinates.get("1.0", "end-1c")
            if needless(userCoor):
                """If the user's input is not given,
                it will generate coordinates randomly
                and print out coordinates in the textfield."""
                self.model.validateEntryCities(self.view.entryCities.get())
                self.model.generateCoordinates()
                self.view.printCoordinates(self.model.coordinates)
            else:    
                self.model.parseCoordinates(userCoor)

            self.iterations = self.model.validateEntryIterations(
                self.view.entryIterations.get())
            self.timer = self.model.validateEntryTimer(
                self.view.entryTimer.get())
        except InvalidIterationInput as E:
            self.view.invalidInput(E)
        except InvalidCityInput as E: 
            self.view.invalidInput(E)
        except InvalidTimerInput as E:
            self.view.invalidInput(E)
        except InvalidCoordinatesIndexInput as E:
            self.view.invalidInput(E)
        except InvalidCoordinatesInput as E:
            self.view.invalidInput(E)
        except InvalidCoordinatesRangeIndexInput as E:
            self.view.invalidInput(E)
        else:
            self.validInput = True


    def reset(self):
        """Resets SOME values to default. The main purpose
        is to observe how iterations, random seeds are influencing the paths.
        It wouldn't be nice to reset all those again for each run.
        Coordinates remain after reset too, the rest is reseted.
        """
        self.view.running = False
        if not self.validInput:
            self.view.defaultTextCoordinates()
        self.validInput = False
        self.view.clearCanvas()
        self.view.stopView()
        self.model.coordinates.clear()
        self.bestPath.clear()
        self.bestDistance = float("inf")
        self.timer = TIMER
        self.iterationCounter = 0
        self.view.updateLabels(0, float("inf"))


    def update(self):
        """This function, called after every iteration (X ms - timer),
        swaps two coordinates.
        If the limit is reached, the iteration stops
        and the best path is rendered.
        """
        if self.iterations <= self.iterationCounter:
            self.view.stopView()
            self.view.drawBestPath(self.bestPath)
            return
        actualDistance = self.model.distance(self.view.lines_id)
        if actualDistance < self.bestDistance:
            self.bestDistance = actualDistance
            self.bestPath = self.model.coordinates[:]

        if self.view.running:
            self.model.shuffle()
            self.view.deleteConnections()
            self.view.connectCities(self.model.coordinates)
            self.view.setTimer(self.timer)
            self.iterationCounter += 1
            self.view.updateLabels(self.iterationCounter, self.bestDistance)


if __name__ == "__main__":
    tsp = Controller()
    tsp.main()