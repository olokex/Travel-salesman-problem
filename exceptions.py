from constants import *

class MyExceptionBase(Exception):
    def __init__(self, input):
        self.base_txt = f"{input} is not valid. "

class InvalidCityInput(MyExceptionBase):
    def __str__(self):
       return self.base_txt + f"Cities has to be {MIN_CITY} or greater."

class InvalidIterationInput(MyExceptionBase):
    def __str__(self):
        return self.base_txt + "Iterations has to be greater or equal than 1."

class InvalidTimerInput(MyExceptionBase):
    def __str__(self):
        return self.base_txt + "Timer has to be greater than 10."

class InvalidCoordinatesInput(Exception):
    def __init__(self, line_idx):
        self.base_txt = f"There must be more than {line_idx} lines to parse coordinates ({MIN_CITY}+)"

    def __str__(self):
        return self.base_txt

class InvalidCoordinatesIndexInput(Exception):
    def __init__(self, line_idx):
        self.base_txt = f"{line_idx+1}. line is incorrect."

    def __str__(self):
        return self.base_txt

class InvalidCoordinatesRangeIndexInput(Exception):
    def __init__(self, line_idx):
        self.base_txt = "{}. line is incorrect. x: {}-{} and y: {}-{}".format(
            line_idx + 1,
            INDENTATION_EDGE,
            WIDTH - INDENTATION_EDGE,
            INDENTATION_EDGE,
            HEIGHT - INDENTATION_EDGE)

    def __str__(self):
        return self.base_txt

class InvalidAreaRange(Exception):
    pass