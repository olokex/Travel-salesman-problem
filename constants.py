#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file is full of constants, which are providing
certain help in one-place modification and default values.
"""

"""10 ms seem like the best lowest working value as refresh rate."""
REFRESH_TIME_MS = 10
ITERATIONS = 1000
CITY_COUNT = 50
"""This size of canvas fits my resolution well."""
WIDTH = 1200
HEIGHT = 800
"""To avoid rendering a city on 0,0 coordinates,
I decided to shrink the canvas area.
"""
INDENTATION_EDGE = 100
BOUNDARY_RIGHT = WIDTH - INDENTATION_EDGE
BOUNDARY_BOT = HEIGHT - INDENTATION_EDGE
BOUNDARY_LEFT = INDENTATION_EDGE
BOUNDARY_TOP = INDENTATION_EDGE
"""Radius for city - circle"""
RADIUS_CITY = 20
"""Less than 4 cities is senseless
connection is always "same" (graph that only rotates the edges).
"""
MIN_CITY_COUNT = 4
DEFAULT_TEXT = f"""\
Line represents
a city.
Each line only one
coordinate x,y.
Coordinates has to  be in certain range
x: {BOUNDARY_LEFT}-{BOUNDARY_RIGHT}
y: {BOUNDARY_TOP}-{BOUNDARY_BOT}

Otherwise gonna be 
generated randomly."""
