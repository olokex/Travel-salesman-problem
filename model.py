from random import randint
import constants

class Model():
    def __init__(self):
        self.coordinates = []
        self.city_count = constants.CITY_COUNT
        self.users_coordinates = False

    def parse_coordinates(self, text):
        tmp = text.split("\n")
        try:
            for each in tmp:
                x, y = each.split(",")
                self.coordinates.append((int(x), int(y)))
        except:
            self.generate_coordinates()

    def generate_coordinates(self):
        for i in range(self.city_count):
            x = randint(constants.INDENTATION_EDGE,
                    constants.WIDTH - constants.INDENTATION_EDGE)
            y = randint(constants.INDENTATION_EDGE,
                    constants.HEIGHT - constants.INDENTATION_EDGE)
            self.coordinates.append((x, y))

    def shuffle(self):
        st = randint(0, len(self.coordinates) - 1)
        nd = randint(0, len(self.coordinates) - 1)
        sc = self.coordinates
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

    def validate():
        ...