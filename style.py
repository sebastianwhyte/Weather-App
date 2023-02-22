PADDING = 10

INVERT = "\033[;7m"
CLEAR = "\033[0m"

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[33m"
WHITE = "\033[37m"


def change_color(color):
	print(color, end="")