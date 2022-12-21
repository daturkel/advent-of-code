#!/usr/bin/env python3

from operator import add, mul, sub, floordiv as div
import sys
from time import perf_counter
from typing import Callable

REV_OP_DICT = {"+": sub, "-": add, "*": div, "/": mul}


def parse_input(lines: dict[str, list[str]]) -> tuple[int, str, dict[str, str]]:
    l, op, r = lines["root"]
    cache = {"humn": "x"}
    parsed_l = parse(l, lines, cache)
    parsed_r = parse(r, lines, cache)

    if "x" in parsed_r:
        known = int(eval(parsed_l))
        unknown = r
    else:
        known = int(eval(parsed_r))
        unknown = l

    return known, unknown, cache


def parse(
    name: str,
    lines: dict[str, list[str]],
    cache: dict,
) -> str:
    if name in cache:
        return cache[name]

    formula = lines[name]

    if len(formula) == 1:
        cache[name] = f"{formula[0]}"
        return cache[name]

    l, op, r = formula
    l_eval = parse(l, lines, cache)
    r_eval = parse(r, lines, cache)
    cache[name] = f"({l_eval} {op} {r_eval})"

    return cache[name]


def invert(lines: dict[str, list[str]], unknown: str, cache) -> list[Callable]:
    ops = []

    get_next_name = lambda x: [
        (key, value) for key, value in lines.items() if x in value
    ][0]

    this_name = "humn"
    next_name, (l, op, r) = get_next_name(this_name)
    while True:
        if this_name == l:
            y = cache[r]

            def f(op, y):
                opf = REV_OP_DICT[op]
                return lambda x: opf(x, y)

            ops.append(f(op, y))
            this_name = next_name
        else:
            y = cache[l]

            def f(op, y):
                opf = REV_OP_DICT[op]

                # there's surely a more graceful way to handle this, but i didn't find it
                trans = lambda x: x
                if op == "-":
                    trans = lambda x: -1 * x
                elif op == "/":
                    trans = lambda x: 1 / x

                return lambda x: opf(trans(x), y)

            ops.append(f(op, y))
            this_name = next_name

        next_name, (l, op, r) = get_next_name(this_name)

        if this_name == unknown:
            break

    return list(reversed(ops))


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines_raw = [line.split() for line in file.readlines()]

    tic = perf_counter()
    lines = {line[0][:-1]: line[1:] for line in lines_raw}
    known, unknown, cache = parse_input(lines)
    numeric_cache = {k: eval(v) for k, v in cache.items() if "x" not in v}

    ops = invert(lines, unknown, numeric_cache)

    result = known
    for i, op in enumerate(ops):
        result = int(op(result))

    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{result=} ({time_us}ms)")
