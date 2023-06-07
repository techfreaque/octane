import enum


class InOutputNodeSides(enum.Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


class Colors(enum.Enum):
    PURPLE = "purple"
    RED = "red"
    GREEN = "green"
    ORANGE = "orange"
    BLUE = "blue"
    CYAN = "cyan"
    YELLOW = "yellow"
    LAWN_GREEN = "LawnGreen"


class InputOutputNodeDirection(enum.Enum):
    IN = "in"
    OUT = "out"


CURRENT_NODES_NAME = "nodes"
