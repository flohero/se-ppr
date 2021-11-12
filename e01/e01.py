import random
from typing import Callable, Generator

options = ("N", "E", "S", "W")


def generate_walk(blocks: int = 1) -> Generator[str, None, None]:
    """
    A function to generate random walks of the length #blocks
    :param blocks: how many blocks should be walked
    :return: a lazy iterator to iterate over the walk
    :raise ValueError: if blocks is lower one
    """
    if blocks < 1:
        raise ValueError("blocks has to be greater than zero")
    for _ in range(blocks):
        yield random.choice(options)


def decode_walk(walk: list) -> tuple[int, int]:
    """
    Decodes a walk into a vector
    :param walk: list containing only the values N, E, S, W
    :return: a vector (x, y)
    """
    if not walk:
        raise ValueError("walk can not be empty")
    options_with_value = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
    dx = 0
    dy = 0
    for direction in walk:
        if direction not in options_with_value:
            raise ValueError("Invalid direction")
        x, y = options_with_value[direction]
        dx += x
        dy += y
    return dx, dy


def distance_manhattan(start: tuple[int, int], end: tuple[int, int]):
    """
    Calculates the manhattan distance for a start and end position
    Here implemented with a loop to support n-dimensional vectors
    :param start: start position
    :param end: end position
    :return: the calculated manhattan distance
    """
    return sum(abs(i1 - i2) for i1, i2 in zip(start, end))


def do_walk(blocks, dist: Callable[[tuple[int, int], tuple[int, int]], int] = distance_manhattan) \
        -> tuple[list[str], int]:
    """
    Generates a walk of the length of blocks and uses the dist function to calculate the distance of the walk
    :param blocks: length of walk
    :param dist: distance function for walk
    :return: a tuple consisting of the walk and its distance
    """
    walk = list(generate_walk(blocks))
    return walk, dist((0, 0), decode_walk(walk))


def monte_carlo_walk_analysis(max_blocks: int, repetitions: int = 10_000) -> dict[int, list[tuple[list[str], int]]]:
    """
    Generate max_blocks * repetitions walks and calculate the distance for each walk
    :param max_blocks: Start with 1 block and generate up to max_block long walks
    :param repetitions: how often a walk of the length of blocks should be generated
    :return: a dictionary, with the longest walk distance as key and the walks as value
    :raise ValueError: if max_blocks or repetitions lower one
    """
    if max_blocks < 1:
        raise ValueError("max_blocks can not be lower one")
    if repetitions < 1:
        raise ValueError("repetitions can not be lower one")
    walks = dict()
    for i in range(1, max_blocks + 1):
        walk_for_blocks = [do_walk(i) for _ in range(repetitions)]
        walks[i] = walk_for_blocks
    return walks


if __name__ == "__main__":
    print("=== Test generate_walk ===")
    print("Test Case 1")
    try:
        print("Expecting Exception")
        generate_walk(blocks=-1).__next__()
    except ValueError as e:
        print("Exception: ", e)

    print("Test Case 2")
    print("Expecting a random list consisting of N, E, S, W: ", list(generate_walk(10)))
    print()

    print("=== Test decode_walk ===")
    print("Test Case 3")
    example_walk = ["N", "N", "N", "W", "W", "W", "S", "S", "S", "E", "E", "E"]
    print("Expecting (0, 0), got ", decode_walk(example_walk))

    print("Test Case 4")
    try:
        print("Expecting Exception")
        decode_walk([])
    except ValueError as e:
        print("Exception: ", e)

    print("Test Case 5")
    try:
        print("Expecting Exception")
        decode_walk(["P"])
    except ValueError as e:
        print("Exception: ", e)

    print()
    print("=== Test distance_manhattan ===")
    print("Test Case 6")
    end_tuple = (7, 7)
    print("Expecting 21, got ", distance_manhattan((3, 4), end_tuple))

    print()
    print("=== Test do_walk ===")
    print("Test Case 7")
    print("Expecting a random walk and distance of zero, got ", do_walk(10, dist=lambda x, y: 0))

    print()
    print("=== Test monte_carlo_walk_analysis ===")
    print("Test Case 8")
    try:
        print("Expecting Exception")
        monte_carlo_walk_analysis(0, 10)
    except ValueError as e:
        print("Exception: ", e)

    print("Test Case 9")
    try:
        print("Expecting Exception")
        monte_carlo_walk_analysis(10, -10)
    except ValueError as e:
        print("Exception: ", e)

    print("Test Case 10")
    print("Expecting a result, got ", monte_carlo_walk_analysis(10, 10))
