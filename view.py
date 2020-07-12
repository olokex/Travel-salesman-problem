#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox 
from constants import *
from utils import *


class View(tk.Tk):
    """Main class for visualization. Responsible for all the components in view,
    which are visible and interactive for user.
    """
    PAD = 3 # Internal padding, mostly for frames. 


    def __init__(self, controller):
        super().__init__()
        self.title("Travel salesman problem")
        self.geometry("1200x800+100+100")
        self.controller = controller
        self.running = False

        self._makeMainFrame()
        self._makeSideFrame()
        self._makeCanvas()
        self._makeCanvasLabels()
        self._makeLabel("Coordinates")
        self._makeTextCoordinates()
        self._makeLabel("Iterations")
        self.entryIterations = self._makeEntry(ITERATIONS)
        self._makeLabel("Cities")
        self.entryCities = self._makeEntry(CITY_COUNT)
        self._makeLabel("Refresh (ms)")
        self.entryREFRESH_TIME_MS = self._makeEntry(REFRESH_TIME_MS)
        self._makeButton("start")
        self._makeButton("reset")


    def main(self):
       self.mainloop()


    def set_refresh(self, REFRESH_TIME_MS):
        """In tkinker you have to re-call a function to keep updated values."""
        self.after_root = self.after(REFRESH_TIME_MS, self.controller.update)


    def stopView(self):
        """Breaks the after call because it was causing a bug."""
        if self.running:
            self.after_cancel(self.after_root)
    

    def clearCanvas(self):
        self.canvas.delete("all")


    def invalidInput(self, message):
        tkinter.messagebox.showerror("Invalid input", message)


    def drawBestPath(self, bestPath):
        """Draws the best path that was found.
        Best path is highlighted with wider red lines.
        I also decided to implement numbers for each city, to indicate
        where to start.
        """
        self.deleteConnections()
        self.connectCities(bestPath, width=3, fill="red")
        self.drawCities(bestPath, colorful=True, width=0)
        self._city_numbers(bestPath)


    def printCoordinates(self, coordinates):
        """Fills textfield with generated coordinates."""
        self.textCoordinates.delete("1.0", "end")
        for coor in coordinates:
            x, y = coor
            txt = f"{x}, {y}\n"
            self.textCoordinates.insert("insert", txt)


    def defaultTextCoordinates(self):
        self.textCoordinates.delete("1.0", "end")
        self.textCoordinates.insert("insert", DEFAULT_TEXT)


    def updateLabels(self, iter, bestDistance):
        self.labelIterationsCanvas["text"] = f"iteration: {iter}"
        dst = f"best distance: {bestDistance:.4f}"
        self.labelBestDistanceCanvas["text"] = dst


    def _makeMainFrame(self):
        self.main_frm = tk.Frame(self)
        self.main_frm.pack(padx=self.PAD, pady=self.PAD)


    def _makeSideFrame(self):
        self.side_frm = tk.Toplevel(self, pady=self.PAD, padx=self.PAD)
        self.side_frm.geometry("+1300+100")
        self.side_frm.title("")


    def _makeEntry(self, text):
        self.ent = tk.Entry(self.side_frm)
        self.ent.insert(0, text)
        self.ent.pack(pady=self.PAD, ipadx=18)
        return self.ent


    def _makeLabel(self, txt):
        lbl = tk.Label(self.side_frm,
            text=txt, font="Helvetica 12")
        lbl.pack(anchor="w")


    def _makeTextCoordinates(self):
        self.textCoordinates = tk.Text(self.side_frm, width=20)
        self.textCoordinates.insert(tk.INSERT, DEFAULT_TEXT)
        self.textCoordinates.pack(pady=self.PAD)


    def _makeButton(self, txt):
        """A bit of an ugly solution for only two buttons...
        This seems more reasonable to me.
        """
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


    def _makeCanvas(self):
        self.canvas = tk.Canvas(
            self.main_frm, width=WIDTH, height=HEIGHT)
        self.canvas.pack()


    def _makeCanvasLabels(self):
        canvas_frame = tk.Frame(self.main_frm)
        canvas_frame.place(x=0, y=HEIGHT-28)
        self.labelIterationsCanvas = tk.Label(
            canvas_frame, text="iteration: 0", font="Helvetica 12")
        self.labelIterationsCanvas.pack(side="left")
        self.labelBestDistanceCanvas = tk.Label(
            canvas_frame, text="best distance: inf", font="Helvetica 12")
        self.labelBestDistanceCanvas.pack(side="left")


    def _create_circle(self, x, y, r=RADIUS_CITY, **kwargs):
        """Tkinter doesn't provide a circle by given x, y and radius
        but only by x1, y1, x2, y2 (impractical).
        I've made my own method that works in that way.
        """
        self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)


    def _city_numbers(self, bestPath):
        """This function adds a number label for each city.
        I decided to make colors to scale with every number.
        It begins with 255 - full red - and substracts for each city.
        """
        col = 255
        for i in range(len(bestPath)):
            label = tk.Label(self.canvas,
                text=i,
                bg=rgb2hex((col, 0, 0)),
                fg="white",
                font="Helvetica 16 bold")
            col -= int(255/len(bestPath) )
            x = bestPath[i][0]
            y = bestPath[i][1]
            self.canvas.create_window(x, y, window=label)


    def drawCities(self, coor, colorful=False, **kwargs):
        """Similar to previous method that scales colors with each city.
        This is similar but only for city - circle
        """
        if colorful:
            color = 255
            for x, y in coor:
                self._create_circle(x, y, 
                    fill=rgb2hex((color, 0 , 0)), **kwargs)
                color -= int(255/len(coor))
        else:        
            for x, y in coor:
                self._create_circle(x, y, RADIUS_CITY, fill="gray", **kwargs)


    def connectCities(self, coor, **kwargs):
        """Each connection has to be stored.
        One possible solution would be to have another frame and clear
        only the frame but this is also usefull for measuring distance in model.
        """
        self.lines_id = {}
        for i in range(len(coor) - 1):
            a = coor[i]
            b = coor[i + 1]
            self.lines_id[a + b] = self.canvas.create_line(a, b, **kwargs)
        a = coor[0]
        b = coor[-1]
        self.lines_id[a + b] = self.canvas.create_line(a, b, **kwargs)


    def deleteConnections(self):
        for key in self.lines_id:
            self.canvas.delete(self.lines_id[key])
        self.lines_id.clear()
