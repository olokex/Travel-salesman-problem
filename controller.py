from model import Model
from view import View
import constants
from utils import *

class Controller():
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.timer = constants.TIMER
        self.iteration_counter = 0
        self.best_distance = float("inf")

    def main(self):
        self.view.main()

    def start(self):
        if self.view.running == True:
            return
        self.view.running = True
        self._get_user_inputs()
        self.view.draw_cities(self.model.coordinates)
        self.view.connect_cities(self.model.coordinates)
        self.view.set_timer(self.timer)

    def _get_user_inputs(self):
        self.model.city_count = validate(self.view.entryCities.get())
        user_coor = self.view.text_coordinates.get("1.0", "end-2c")
        self.model.parse_coordinates(user_coor)

        #self.model.validate(self.view.entryCities.get(),
        #    self.view.entryTimer.get(),
        #    self.view.entryIterations.get()
        #)
        #print(self.model.city_count)
        self.timer = validate(self.view.entryTimer.get())
        self.iterations = validate(self.view.entryIterations.get())

    def reset(self):
        self.view.running = False
        self.view.clear_canvas()
        self.model.coordinates.clear()
        self.best_path.clear()
        self.best_distance = float("inf")
        self.timer = constants.TIMER
        self.iteration_counter = 0
        self.view.update_labels(0, float("inf"))

    def update(self):
        if not (self.iterations > self.iteration_counter):
            self.view.stop_view()
            self.view.draw_best_path(self.best_path)
            return

        self.model.shuffle()
        self.view.delete_connections()
        self.view.connect_cities(self.model.coordinates)
        self.view.set_timer(self.timer)
        self.iteration_counter += 1
        actual_distance = self.model.distance(self.view.lines_id)
        if actual_distance < self.best_distance:
            self.best_distance = actual_distance
            self.best_path = self.model.coordinates
        self.view.update_labels(self.iteration_counter, self.best_distance)

def validate(string):
    return int(string)

if __name__ == "__main__":
    tsp = Controller()
    tsp.main()