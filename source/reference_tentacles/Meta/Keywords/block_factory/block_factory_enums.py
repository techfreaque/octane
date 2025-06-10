import enum


class InOutputNodeSides(enum.Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


class Colors(enum.Enum):
    AZURE = "azure"
    BEIGE = "beige"
    BLACK = "black"
    BLUE = "blue"
    BROWN = "brown"
    CORAL = "coral"
    CYAN = "cyan"
    GREEN = "green"
    GREY = "grey"
    GOLD = "gold"
    LAVENDER = "lavender"
    LIME = "lime"
    MAROON = "maroon"
    OLIVE = "olive"
    ORANGE = "orange"
    ORCHID = "orchid"
    PINK = "pink"
    PURPLE = "purple"
    RED = "red"
    SALMON = "salmon"
    SILVER = "silver"
    TURQUOISE = "turquoise"
    WHEAT = "wheat"
    WHITE = "white"
    YELLOW = "yellow"


class InputOutputNodeDirection(enum.Enum):
    IN = "in"
    OUT = "out"


CURRENT_NODES_NAME = "nodes"

MODE_CONFIG_NAME = "mode_node"
CURRENT_NODE_CONFIG_NAME = f"config_{MODE_CONFIG_NAME}"
