"""
These are values used to express non-printable key values such as
left arrow, right arrow, home, end, etc.
"""

UNKNOWN_KEY = -1

# ASCII values
BACKSPACE = 8
TAB = 9
ENTER = 13
ESCAPE = 27
DELETE = 127

LEFT_ARROW = 256
RIGHT_ARROW = LEFT_ARROW + 1
UP_ARROW = LEFT_ARROW + 2
DOWN_ARROW = LEFT_ARROW + 3

FUNC_0 = DOWN_ARROW + 1
FUNC_1 = FUNC_0 + 1
FUNC_2 = FUNC_0 + 2
FUNC_3 = FUNC_0 + 3
FUNC_4 = FUNC_0 + 4
FUNC_5 = FUNC_0 + 5
FUNC_6 = FUNC_0 + 6
FUNC_7 = FUNC_0 + 7
FUNC_8 = FUNC_0 + 8
FUNC_9 = FUNC_0 + 9
FUNC_10 = FUNC_0 + 10
FUNC_11 = FUNC_0 + 11
FUNC_12 = FUNC_0 + 12
FUNC_13 = FUNC_0 + 13
FUNC_14 = FUNC_0 + 14

HOME = FUNC_14 + 1
END = HOME + 1
PAGE_UP = HOME + 2
PAGE_DOWN = HOME + 3
