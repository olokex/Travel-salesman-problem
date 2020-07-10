#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
from constants import *
from exceptions import *
from math import sqrt


class Model():
    """Main Model class responsible for business logic."""


    def __init__(self):
        self.coordinates = []
        self.cityCount = CITY_COUNT
        self.userCoordinates = False


    def parseCoordinates(self, text):
        lines = text.splitlines()
        count = len(lines)
        if count < MIN_CITY:
            raise InvalidCoordinatesInput(count)

        for i, line in enumerate(lines):
            try:
                coor = line.strip().split(",")
                x = int(coor[0])
                y = int(coor[1])
                self._isInAllowedRange(x, WIDTH_MIN, WIDTH_MAX)
                self._isInAllowedRange(y, HEIGHT_MIN, HEIGHT_MAX)
                self.coordinates.append((x, y))
            except InvalidAreaRange:
                raise InvalidCoordinatesRangeIndexInput(i)
            except Exception:
                raise InvalidCoordinatesIndexInput(i)
        self.cityCount = len(self.coordinates)


    def _isInAllowedRange(self, var, min, max):
        if not (min <= var <= max):
            raise InvalidAreaRange


    def generateCoordinates(self):
        """Generates coordinates x,y in shrinked area, 100 px from each side.
        Avoids generating city with 0,0; 0,Y; X,0; etc.
        """
        for i in range(self.cityCount):
            x = randint(WIDTH_MIN, WIDTH_MAX)
            y = randint(HEIGHT_MIN, HEIGHT_MAX)
            self.coordinates.append((x, y))

    def shuffle(self):
        """Randomly swaps two coordinates - new path is established."""
        sc = self.coordinates
        st = randint(0, len(sc) - 1)
        nd = randint(0, len(sc) - 1)
        sc[st], sc[nd] = sc[nd], sc[st]

    def _distanceTwoPoints(self, coordinates):
        """Nothing but Pythagoras theorem."""
        x1 = coordinates[0]
        y1 = coordinates[1]
        x2 = coordinates[2]
        y2 = coordinates[3]
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def distance(self, lines_id):
        dist = 0.0
        for coor in lines_id.keys():
            dist += self._distanceTwoPoints(coor)
        return dist

    def validateEntryCities(self, input):
        if not input.isdigit():
            raise InvalidCityInput(input)
        cityCount = int(input)
        if not (cityCount >= MIN_CITY):
            raise InvalidCityInput(input)
        self.cityCount = cityCount


    def validateEntryTimer(self, input):
        if not input.isdigit():
            raise InvalidTimerInput(input)    
        timer = int(input)
        if not (timer >= 10):
            raise InvalidTimerInput(input)    
        return timer

    def validateEntryIterations(self, input):
        if not input.isdigit():
            raise InvalidIterationInput(input)    
        iteration = int(input)
        if not (iteration >= 1):
            raise InvalidIterationInput(input)    
        return iteration
