#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from constants import *


class MyExceptionBase(Exception):
    def __init__(self, input):
        self.baseTxt = f"{input} is not valid. "


class InvalidCityInput(MyExceptionBase):
    def __str__(self):
       return self.baseTxt + f"Cities have to be {MIN_CITY} or greater."


class InvalidIterationInput(MyExceptionBase):
    def __str__(self):
        return self.baseTxt + "Iterations have to be greater or equal than 1."


class InvalidTimerInput(MyExceptionBase):
    def __str__(self):
        return self.baseTxt + "Timer has to be greater than 10."


class InvalidCoordinatesInput(Exception):
    def __init__(self, lineIndex):
        self.baseTxt = f"There must be more than {lineIndex} lines to parse coordinates ({MIN_CITY}+)"

    def __str__(self):
        return self.baseTxt


class InvalidCoordinatesIndexInput(Exception):
    def __init__(self, lineIndex):
        self.baseTxt = f"{lineIndex+1}. line is incorrect."

    def __str__(self):
        return self.baseTxt


class InvalidCoordinatesRangeIndexInput(Exception):
    def __init__(self, lineIndex):
        self.baseTxt = "{}. line is incorrect. x: {}-{} and y: {}-{}".format(
            lineIndex + 1,
            INDENTATION_EDGE,
            WIDTH - INDENTATION_EDGE,
            INDENTATION_EDGE,
            HEIGHT - INDENTATION_EDGE)

    def __str__(self):
        return self.baseTxt


class InvalidAreaRange(Exception):
    pass
