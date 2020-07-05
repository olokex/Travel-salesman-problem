from model import Model
from view import View
from constants import *
from utils import *
from exceptions import *

class Controller():
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.timer = TIMER
        self.iteration_counter = 0
        self.best_distance = float("inf")
        self.valid_input = False
        self.best_path = []

    def main(self):
        self.view.main()

    def start(self):
        if self.view.running == True:
            return
        self._get_user_inputs()
        if self.valid_input == False:
            return
        self.view.running = True
        self.view.draw_cities(self.model.coordinates)
        self.view.connect_cities(self.model.coordinates)
        self.view.set_timer(self.timer)

    def _get_user_inputs(self):
        try:
            user_coor = self.view.text_coordinates.get("1.0", "end-1c")
            if needless(user_coor):
                self.model.validate_entryCities(self.view.entryCities.get())
                self.model.generate_coordinates()
            else:    
                self.model.parse_coordinates(user_coor)

            self.iterations = self.model.validate_entryIterations(
                self.view.entryIterations.get())
            self.timer = self.model.validate_entryTimer(
                self.view.entryTimer.get())
        except InvalidIterationInput as E:
            self.view.invalid_input(E)
        except InvalidCityInput as E: 
            self.view.invalid_input(E)
        except InvalidTimerInput as E:
            self.view.invalid_input(E)
        except InvalidCoordinatesIndexInput as E:
            self.view.invalid_input(E)
        except InvalidCoordinatesInput as E:
            self.view.invalid_input(E)
        except InvalidCoordinatesRangeIndexInput as E:
            self.view.invalid_input(E)
        else:
            self.valid_input = True

    def reset(self):
        self.view.running = False
        self.valid_input = False
        self.view.clear_canvas()
        self.view.stop_view()
        self.model.coordinates.clear()
        self.best_path.clear()
        self.best_distance = float("inf")
        self.timer = TIMER
        self.iteration_counter = 0
        self.view.update_labels(0, float("inf"))

    def update(self):
        actual_distance = self.model.distance(self.view.lines_id)
        if actual_distance < self.best_distance:
            self.best_distance = actual_distance
            self.best_path = self.model.coordinates[:]
        if not (self.iterations > self.iteration_counter):
            self.view.stop_view()
            self.view.draw_best_path(self.best_path)
            return

        self.model.shuffle()
        self.view.delete_connections()
        self.view.connect_cities(self.model.coordinates)
        self.view.set_timer(self.timer)
        self.iteration_counter += 1
        self.view.update_labels(self.iteration_counter, self.best_distance)

if __name__ == "__main__":
    tsp = Controller()
    tsp.main()