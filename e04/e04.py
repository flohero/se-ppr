import random
import tracemalloc
from typing import Callable, Generator, Optional

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


def do_walk(blocks, dist: Callable[[tuple[int, int], tuple[int, int]], int] = distance_manhattan, gen_walk=True) \
        -> tuple[Optional[list[str]], int]:
    """
    Generates a walk of the length of blocks and uses the dist function to calculate the distance of the walk
    :param blocks: length of walk
    :param dist: distance function for walk
    :param gen_walk: if set to true the generated walk is returned, else only the distance is returned
    :return: a tuple consisting of the walk and its distance
    """
    walk = generate_walk(blocks)
    if gen_walk:
        walk = list(walk)
    start = (0, 0)
    if gen_walk:
        return walk, dist(start, decode_walk(walk))
    else:
        return None, dist(start, decode_walk(walk))


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
        walk_for_blocks = [do_walk(i, gen_walk=True) for _ in range(repetitions)]
        walks[i] = walk_for_blocks
    return walks


def monte_carlo_walk(max_blocks: int, repetitions: int = 10_000) -> dict[int, list[int]]:
    """
    Generate max_blocks * repetitions walks and calculate the distance for each walk
    :param max_blocks: Start with 1 block and generate up to max_block long walks
    :param repetitions: how often a walk of the length of blocks should be generated
    :return: a dictionary, with the longest walk distance as key and the walk distances for each walk, omitting the actual walk
    :raise ValueError: if max_blocks or repetitions lower one
    """
    if max_blocks < 1:
        raise ValueError("max_blocks can not be lower one")
    if repetitions < 1:
        raise ValueError("repetitions can not be lower one")
    walks = dict()
    for i in range(1, max_blocks + 1):
        walk_for_blocks = [do_walk(i, gen_walk=False)[1] for _ in range(repetitions)]
        walks[i] = walk_for_blocks
    return walks


if __name__ == "__main__":
    tracemalloc.start()

    monte_carlo_walk_analysis(20)
    _, peak = tracemalloc.get_traced_memory()
    print("Traced Memory Peak of monte_carlo_walk_analysis:", peak)
    snapshot1 = tracemalloc.take_snapshot()
    tracemalloc.reset_peak()

    monte_carlo_walk(20)
    _, peak = tracemalloc.get_traced_memory()
    print("Traced Memory Peak of monte_carlo_walk:", peak)
    snapshot2 = tracemalloc.take_snapshot()
    top_stats = snapshot2.compare_to(snapshot1, 'traceback')

    print("Allocations per Line")
    for stat in top_stats:
        print(stat)
