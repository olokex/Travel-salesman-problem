# Travel salesman problem
### Description
This problem is well known [I recommend read about theory there](https://simple.wikipedia.org/wiki/Travelling_salesman_problem). 

This program works on Monte Carlo basis, where path is defined as coordinates in array and randomly swapping two coordinates `(Xn, Yn) <-> (Xm, Ym)`, so we don't have to deal with verifying if the path is visited only once etc.

### Algorithm
1. Generate random list of coordinates
...can be user's input as well
2. Make sum of distance
3. If distance is better than the shortes:
...store list of coordinates (copy)
...store the best distance
4. Randomly swap two coordinates
5. If there iterations left goto 2. else terminate
6. Print out the best path and distance

### Reason
_Created with the purpose of studying MVC and OOP in Python with tkinter as GUI._

## Run and usage
Required **Python 3.7+** tkinter should be included in standard library.
For running the code open terminal in project folder and type `python controller.py`
