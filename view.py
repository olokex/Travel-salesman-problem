#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox 
from constants import *
from utils import *

class View(tk.Tk):
    PAD = 3

    def __init__(self, controller):
        super().__init__()
        self.title("Travel salesman problem")
        self.geometry("1200x800+100+100")
        self.controller = controller
        self.running = False

        self._make_main_frame()
        self._make_side_frame()
        self._make_canvas()
        self._make_canvas_labels()
        self._make_label("Coordinates")
        self._make_text_coordinates()
        self._make_label("Iterations")
        self.entryIterations = self._make_entry(ITERATIONS)
        self._make_label("Cities")
        self.entryCities = self._make_entry(CITY_COUNT)
        self._make_label("Timer (ms)")
        self.entryTimer = self._make_entry(TIMER)
        self._make_button("start")
        self._make_button("reset")

    def main(self):
       self.mainloop()

    def set_timer(self, timer):
        # In tkinker you have to re-call a function to keep updated values.
        self.after_root = self.after(timer, self.controller.update)

    def stop_view(self):
        # Breaks the after call because was causing a bug.
        if self.running:
            self.after_cancel(self.after_root)
    
    def clear_canvas(self):
        self.canvas.delete("all")

    def invalid_input(self, message):
        tkinter.messagebox.showerror("Invalid input", message)

    def draw_best_path(self, best_path):
        # Draws the best path that was found.
        # Best path is highlighted with red and wider line,
        # also decided to implement numbers for each city (where to start).
        self.delete_connections()
        self.connect_cities(best_path, width=3, fill="red")
        self.draw_cities(best_path, colorful=True, width=0)
        self._city_numbers(best_path)

    def print_coordinates(self, coordinates):
        # Fill textfield with coordinates which were generated.
        self.text_coordinates.delete("1.0", "end")
        for coor in sorted(coordinates):
            x, y = coor
            txt = f"{x}, {y}\n"
            self.text_coordinates.insert("insert", txt)

    def default_text_coordinates(self):
        self.text_coordinates.delete("1.0", "end")
        self.text_coordinates.insert("insert", DEFAULT_TEXT)


    def update_labels(self, iter, best_distance):
        self.labelIterationsCanvas["text"] = f"iteration: {iter}"
        dst = f"best distance: {best_distance:.4f}"
        self.labelBestDistanceCanvas["text"] = dst

    def _make_main_frame(self):
        self.main_frm = tk.Frame(self)
        self.main_frm.pack(padx=self.PAD, pady=self.PAD)

    def _make_side_frame(self):
        self.side_frm = tk.Toplevel(self, pady=self.PAD, padx=self.PAD)
        self.side_frm.geometry("+1300+100")
        self.side_frm.title("")

    def _make_entry(self, text):
        self.ent = tk.Entry(self.side_frm)
        self.ent.insert(0, text)
        self.ent.pack(pady=self.PAD, ipadx=18)
        return self.ent

    def _make_label(self, txt):
        lbl = tk.Label(self.side_frm,
            text=txt, font="Helvetica 12")
        lbl.pack(anchor="w")

    def _make_text_coordinates(self):
        self.text_coordinates = tk.Text(self.side_frm, width=20)
        self.text_coordinates.insert(tk.INSERT, DEFAULT_TEXT)
        self.text_coordinates.pack(pady=self.PAD)

    def _make_button(self, txt):
        # A bit ugly solution but only for two buttons...
        # This seems more reasonable to me.
        cmd = self.controller.start
        if txt == "reset":
            cmd = self.controller.reset
        btn = tk.Button(self.side_frm,
                width = 8, 
                bd = 0,
                relief = "flat",
                font = "Helvetica 12",
                text = txt,
                command = cmd)
        btn.pack(side="left")

    def _make_canvas(self):
        self.canvas = tk.Canvas(
            self.main_frm, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

    def _make_canvas_labels(self):
        canvas_frame = tk.Frame(self.main_frm)
        canvas_frame.place(x=0, y=HEIGHT-28)
        self.labelIterationsCanvas = tk.Label(
            canvas_frame, text="iteration: 0", font="Helvetica 12")
        self.labelIterationsCanvas.pack(side="left")
        self.labelBestDistanceCanvas = tk.Label(
            canvas_frame, text="best distance: inf", font="Helvetica 12")
        self.labelBestDistanceCanvas.pack(side="left")

    def _create_circle(self, x, y, r=RADIUS, **kwargs):
        # Because tkinter doesn't provide a circle by given x, y and radius
        # but only by x1, y1, x2, y3 (impractical).
        # I've made my own method that works in this way.
        self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def _city_numbers(self, best_path):
        # This function add a number label for each city.
        # I decided to make colors to scale with every number.
        # It begins with 255 - full red here, and is substracting for each city.
        col = 255
        for i in range(len(best_path)):
            label = tk.Label(self.canvas,
                text=i,
                bg=rgb2hex((col, 0, 0)),
                fg="white",
                font="Helvetica 16 bold")
            col -= int(255/len(best_path) )
            x = best_path[i][0]
            y = best_path[i][1]
            self.canvas.create_window(x, y, window=label)

    def draw_cities(self, coor, colorful=False, **kwargs):
        # Similar to previous method that scale colors with each city.
        # This is similar but only for city - circle
        if colorful:
            color = 255
            for x, y in coor:
                self._create_circle(x, y, 
                    fill=rgb2hex((color, 0 , 0)), **kwargs)
                color -= int(255/len(coor))
        else:        
            for x, y in coor:
                self._create_circle(x, y, RADIUS, fill="gray", **kwargs)

    def connect_cities(self, coor, **kwargs):
        # Each connection have to be stored.
        # One possible solution would be have another frame and clear
        # only the fram but this is also usefull for measuring distance in model
        self.lines_id = {}
        for i in range(len(coor) - 1):
            a = coor[i]
            b = coor[i + 1]
            self.lines_id[a + b] = self.canvas.create_line(a, b, **kwargs)
        a = coor[0]
        b = coor[-1]
        self.lines_id[a + b] = self.canvas.create_line(a, b, **kwargs)

    def delete_connections(self):
        for key in self.lines_id:
            self.canvas.delete(self.lines_id[key])
        self.lines_id.clear()
