import sys
from time import perf_counter


def solve(lines: list[str], x: int) -> tuple[int, int]:
    part_one = 1
    points = []
    distances = dict()
    # parse input
    for line in lines:
        points.append(tuple(int(coord) for coord in line.split(",")))

    # calculate distances
    for i, (x1, y1, z1) in enumerate(points):
        for j, (x2, y2, z2) in enumerate(points[i + 1 :], start=i + 1):
            distances[(i, j)] = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2

    # assemble circuits
    num_circuits = len(points)
    # list of sets
    circuits = [set([i]) for i in range(len(points))]
    # map of point index to circuit index
    circuit_map = {i: i for i in range(len(points))}
    # sort the distances descending, it's not that slow
    for ix, ((i, j), _) in enumerate(sorted(distances.items(), key=lambda x: x[1])):
        i_ix = circuit_map[i]
        j_ix = circuit_map[j]
        i_circuit = circuits[i_ix]
        j_circuit = circuits[j_ix]
        # continue if they're already in the same circuit
        if i_ix == j_ix:
            continue
        # combine the circuits, moving the elements in the smaller one to the bigger one
        if len(j_circuit) > len(i_circuit):
            for elem in i_circuit:
                circuit_map[elem] = j_ix
            circuits[i_ix] = None  # type: ignore
            circuits[j_ix] = i_circuit.union(j_circuit)
        else:
            for elem in j_circuit:
                circuit_map[elem] = i_ix
            circuits[j_ix] = None  # type: ignore
            circuits[i_ix] = i_circuit.union(j_circuit)
        # solve part one
        if ix == x - 1:
            for i, circuit in enumerate(
                sorted(filter(bool, circuits), key=len, reverse=True)
            ):
                if i < 3:
                    part_one *= len(circuit)
        num_circuits -= 1
        # stop if we're down to one circuit
        if num_circuits == 1:
            break

    part_two = points[i][0] * points[j][0]
    return part_one, part_two


if __name__ == "__main__":
    input_file, x = (sys.argv[1], 1000) if len(sys.argv) > 1 else ("./test.txt", 10)
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines, x)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
