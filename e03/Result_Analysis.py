#!/usr/bin/env python
# coding: utf-8

# # Exercise 03
# ## Setup
# Start a walk up to 50 blocks, and execute every maximum block 10.000 times.


import e01.e01 as mc

walks = mc.monte_carlo_walk_analysis(50, 10_000)

# ## 01
# How many roundtrips of length 4 (including duplicates) have been generated?
# Roundtrips  are  tours  of  a  distance  of  zero  from  the  starting  position  and  the
# length of a roundtrip is the number of walked blocks.
# 
# All trips of max length 4 are saved in the dictionary at the key 4.
# Iterate over the trips and check if the calculated distance is zero, these are the roundtrips.


roundtrip_length_4 = [walk for walk, dist in walks[4] if dist == 0]

# Number of roundtrips with max length 4


len(roundtrip_length_4)

# ## 02
# Which  different  (unique)  roundtrips  have  been  identified  for  the  different
# maximum  lengths?  List  the  number  of  identified  unique  roundtrips  for  each
# maximum  length  and  the  first  10  roundtrips  per  maximum  length  (the  others
# can be omitted).
# 
# ### Notes
# All roundtrips have to have an even number of steps,
# therefore it is possible to ignore all walks with an odd number of maximum steps.
# 
# ### All Roundtrips
# First all roundtrips have to be calculated, while preserving the original data structures.
# This is again done by checking if the distance is zero for each walk.
# To optimize the algorithm it is possible to ignore all trips with an odd max distance.


all_roundtrips = {key: [walk for walk, length in walks[key] if length == 0] for key in walks if key % 2 == 0}

# To get the top 10 roundtrips for each max length, just slice the walk array for every max distance.


top_10_roundtrips = {key: all_roundtrips[key][:10] for key in all_roundtrips}

# To get all unique roundtrips, each walk has to be converted to a tuple and then saved into a set,
# which guarantees that duplicated walks will be removed.
# The walks will be converted to a list and put into another list.
# The result will be a list of lists with unqiue roundtrips


unique_roundtrips = [list(x) for x in
                     set(tuple(x) for x in [walk for key in all_roundtrips for walk in all_roundtrips[key]])]

# Number of unique roundtrips


len(unique_roundtrips)

# Top 10 Roundtrips for each max distance


top_10_roundtrips

# ## 03
# What is the average and median1 distance for walks of maximum lengths 5, 10, 15, 20, 25?
# 
# Define a function which outputs average and median of a list of walks with their distance.
# The functions puts all distances for each walk into a list and sorts that list.
# Then using the statistics package the median and average are calculated.
# This is done for walks of max length 5, 10, 15, 20, 25


import statistics


def average_median(w: list[tuple[list[str], int]]) -> None:
    distances = sorted([dist for walk, dist in w])
    print("Average: ", statistics.mean(distances))
    print("Median1", statistics.median(distances))


print("Walks of 5")
walks5 = walks[5]
average_median(walks5)
print()

print("Walks of 10")
walks10 = walks[10]
average_median(walks10)
print()

print("Walks of 15")
walks15 = walks[15]
average_median(walks15)
print()

print("Walks of 20")
walks20 = walks[20]
average_median(walks20)
print()

print("Walks of 25")
walks25 = walks[25]
average_median(walks25)

# ## 04
# What is the percentage of walks that end at a position with a maximum possible
# distance from the starting distance per maximum walk length?
# 
# First flatten the walks dictionary, so all walk lists are in the resulting list and the calculate the length,
# so we have the total number of walks.
# This can also be done by multiplying 50 * 10.000, but this way we can be sure.


total_number_of_walks = len([walk for key in walks for walk, dist in walks[key]])

# Then find all walks, which have reached the max distance,
# this is done by iterating over the walks dictionary
# and checking if the distance of each walk is the same as the key of the dictionary.


walks_with_max_dist = [walk for key in walks for walk, dist in walks[key] if dist == key]

# Percentage of max walks


f"{round((len(walks_with_max_dist) / total_number_of_walks) * 100, 2)}%"


# ## 05
# Which distinct straight walks have been generated; walks that continue in the
# same direction? Therefore, you have to implement a predicate function
# `def checkEqual(iterator)` that checks whether an iterator consists only of
# one  different  element.  Try  to  avoid  additional  memory  allocation  within  the
# checkEqual function.
# 
# First implement the `check_equal` function, it checks if each element is qualto the first in an iterator.
# Then iterate over each walk and use the `check_equal` function to check if they are straight walks.
# To check if the walks are distinct use the same algorithm as in task 02.
# Convert each walk into a tuple, put them into a set
#  and then convert each tuple back into a list and put the resulting lists into another list.


def check_equal(iterator) -> bool:
    if len(iterator) == 0:
        return True
    for d in iterator:
        if d != iterator[0]:
            return False
    return True


straight_walks = [list(x) for x in set(tuple(walk) for key in walks for walk, dist in walks[key] if check_equal(walk))]
sorted(straight_walks)
