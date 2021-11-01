import turtle
from typing import Union

from matplotlib.colors import Colormap, LinearSegmentedColormap, ListedColormap

import matplotlib.pyplot as plt

from e01.e01 import generate_walk


def setup_screen():
    """
    Set screen size
    :return:
    """
    screen = turtle.Screen()
    screen.screensize(500, 500)


def generate_distinct_colors(n: int) -> Union[Colormap, LinearSegmentedColormap, ListedColormap]:
    """
    Function to generate function, which maps each index 0...n-1 to distinct colors
    :param n: number of distinct colors
    :return: function to map the index to a color
    """
    return plt.get_cmap(lut=n, name="tab20c")


def turtle_go_to_position(t: turtle.Turtle, x: float, y: float):
    """
    Go to a position without drawing something
    :param t: turtle
    :param x: x coordinate
    :param y: y coordinate
    :return:
    """
    t.penup()
    t.setposition(x, y)
    t.pendown()


def set_up_turtle(t: turtle.Turtle, color: tuple[float, float, float, float], offset: float = 0.0,
                  thickness: int = 3) -> None:
    """
    Set the turtle up before it starts to draw the walk
    :param t: the turtle
    :param color: color of the pen, here with alpha channel, which will be ignored
    :param offset: the offset to the starting position, so multiple graphs don't overlap
    :param thickness: thickness of the pen
    :return:
    """
    t.hideturtle()
    t.color(color[:-1])
    t.pensize(thickness)
    turtle_go_to_position(t, offset, offset)
    t.showturtle()


def draw_legend_for_walk(t: turtle.Turtle, turtle_nr: int, window_offset: float = 20, line_offset: float = 10) -> None:
    """
    Draws for one turtle the legend, which includes color and index of the turtle
    :param t: the turtle
    :param turtle_nr: the index of this turtle
    :param window_offset: the offset from the upper left corner of the window
    :param line_offset: how much space between the lines of the legend is left
    :return:
    """
    old_x, old_y = t.pos()
    x = -turtle.window_width() / 2 + window_offset
    y = turtle.window_height() / 2 - (t.pensize() * turtle_nr * line_offset) - window_offset

    turtle_go_to_position(t, x, y)
    t.dot(8)

    turtle_go_to_position(t, x + t.pensize() * 2, y)
    t.write(f"Turtle #{turtle_nr}", move=False, align="left", font=("Arial", 12, "bold"))
    turtle_go_to_position(t, old_x, old_y)


def draw_walk(walk: list[str], t: turtle.Turtle, length: int = 100) -> None:
    """
    Lets a turtle walk in a direction for the length
    :param walk: the directions
    :param t: turtle to draw the graph
    :param length: how long the lines in each direction will be
    """
    if length <= 0:
        raise ValueError("Invalid walking length")
    directions = {
        'N': 90,
        'E': 0,
        'S': 270,
        'W': 180
    }
    t.dot()
    for direction in walk:
        if direction not in directions:
            raise ValueError("Invalid direction")
        t.setheading(directions[direction])
        t.forward(length)
    t.dot()


def draw_multiple_walks(walks: list[list[str]]) -> None:
    """
    Draws multiple walks with a distinct color
    :param walks: the walks
    :return:
    """
    n_colors = generate_distinct_colors(len(walks))
    setup_screen()
    t = turtle.Turtle()
    for i in range(len(walks)):
        set_up_turtle(t, n_colors(i), 4 * i)
        draw_legend_for_walk(t, i)
        draw_walk(walks[i], t)


if __name__ == "__main__":
    blocks = 10
    walk_count = 10
    generated_walks = [list(generate_walk(blocks)) for _ in range(walk_count)]
    draw_walk(generated_walks[0], turtle.Turtle())
    #draw_multiple_walks(generated_walks)
    turtle.mainloop()
