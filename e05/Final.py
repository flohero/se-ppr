import e04.Memory as mcw

if __name__ == "__main__":
    full_output = True
    for run in range(0, 10):
        print(f"Run #{run}")
        distance = 50
        iterations = 10_000
        walk_length_condition = 6
        print(f"Running monte carlo walk with params: max_distance={distance}, iterations={iterations}, "
              f"walk_length_condition={walk_length_condition}")
        walks = mcw.monte_carlo_walk(distance, iterations)
        for k, v in walks.items():
            total_walks_of_length = len(v)
            number_of_walks_under_max_dist = 0
            for length in v:
                if length <= walk_length_condition:
                    number_of_walks_under_max_dist += 1
            if full_output:
                print(f"Walks of length {k:2} are with a probability of " +
                      f"{number_of_walks_under_max_dist/total_walks_of_length * 100:6.2f}% short.")
            else:
                print(f"{number_of_walks_under_max_dist/total_walks_of_length:6.4f}")
