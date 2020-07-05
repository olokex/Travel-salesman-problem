from random import randint
from constants import *
from exceptions import *

class Model():
    def __init__(self):
        self.coordinates = []
        self.city_count = CITY_COUNT
        self.users_coordinates = False

    def parse_coordinates(self, text):
        lines = text.splitlines()
        count = len(lines)
        if count < MIN_CITY:
            raise InvalidCoordinatesInput(count)

        for i, line in enumerate(lines):
            try:
                coor = line.strip().split(",")
                x = int(coor[0])
                y = int(coor[1])
                self._in_allowed_range(x, WIDTH_MIN, WIDTH_MAX)
                self._in_allowed_range(y, HEIGHT_MIN, HEIGHT_MAX)
                self.coordinates.append((x, y))
            except InvalidAreaRange:
                raise InvalidCoordinatesRangeIndexInput(i)
            except Exception:
                raise InvalidCoordinatesIndexInput(i)
        self.city_count = len(self.coordinates)


    def _in_allowed_range(self, var, min, max):
        if not (min <= var <= max):
            raise InvalidAreaRange


    def generate_coordinates(self):
        for i in range(self.city_count):
            x = randint(WIDTH_MIN, WIDTH_MAX)
            y = randint(HEIGHT_MIN, HEIGHT_MAX)
            self.coordinates.append((x, y))

    def shuffle(self):
        sc = self.coordinates
        st = randint(0, len(sc) - 1)
        nd = randint(0, len(sc) - 1)
        sc[st], sc[nd] = sc[nd], sc[st]

    def _distance_two_points(self, coordinates):
            x1 = coordinates[0]
            y1 = coordinates[1]
            x2 = coordinates[2]
            y2 = coordinates[3]
            return ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)

    def distance(self, lines_id):
        dist = 0.0
        for coor in lines_id.keys():
            dist += self._distance_two_points(coor)
        return dist

    def validate_entryCities(self, input):
        if not input.isdigit():
            raise InvalidCityInput(input)
        city_count = int(input)
        if not (city_count >= MIN_CITY):
            raise InvalidCityInput(input)
        self.city_count = city_count


    def validate_entryTimer(self, input):
        if not input.isdigit():
            raise InvalidTimerInput(input)    
        timer = int(input)
        if not (timer >= 10):
            raise InvalidTimerInput(input)    
        return timer

    def validate_entryIterations(self, input):
        if not input.isdigit():
            raise InvalidIterationInput(input)    
        iteration = int(input)
        if not (iteration >= 1):
            raise InvalidIterationInput(input)    
        return iteration