#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from model import Model
from view import View
from constants import *
from utils import *
from exceptions import *

class Controller():
    # Main class that controlls all the events.
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.timer = TIMER
        self.iteration_counter = 0
        # Distance has to start with high number,
        # because even the first one can be the shortest.
        self.best_distance = float("inf")
        # Check for user's input.
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
        # Validates user's input
        # for futher info read constants.py and model.
        try:
            user_coor = self.view.text_coordinates.get("1.0", "end-1c")
            if needless(user_coor):
                # If there is not user's input
                # it will generate coordinates randomly
                # and print out coordinates in the textfield.
                self.model.validate_entryCities(self.view.entryCities.get())
                self.model.generate_coordinates()
                self.view.print_coordinates(self.model.coordinates)
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
        # Resets NOT all the values to default the main purpose
        # is to observe how iterations, random seed are influencing the paths
        # wouldn't be nice to reset all those again for each run.
        # Coordinates remains after reset too, rest is reseted.
        self.view.running = False
        if not self.valid_input:
            self.view.default_text_coordinates()
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
        # This function is called after every iteration (X ms - timer),
        # where two coordinates are swapped.
        # If the limit is reached, iteration stops and the best path rendered.
        if not (self.iterations > self.iteration_counter):
            self.view.stop_view()
            self.view.draw_best_path(self.best_path)
            return
        actual_distance = self.model.distance(self.view.lines_id)
        if actual_distance < self.best_distance:
            self.best_distance = actual_distance
            self.best_path = self.model.coordinates[:]

        if self.view.running:
            self.model.shuffle()
            self.view.delete_connections()
            self.view.connect_cities(self.model.coordinates)
            self.view.set_timer(self.timer)
            self.iteration_counter += 1
            self.view.update_labels(self.iteration_counter, self.best_distance)

if __name__ == "__main__":
    tsp = Controller()
    tsp.main()