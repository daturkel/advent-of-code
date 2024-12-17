import sys
from time import perf_counter


def combo(x: int, a: int, b: int, c: int) -> int:
    if x < 4:
        return x
    elif x == 4:
        return a
    elif x == 5:
        return b
    elif x == 6:
        return c
    else:
        raise RuntimeError("invalid combo")


opname = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]


def execute(
    program: list[int], a: int, b: int, c: int, debug: bool = False
) -> list[int]:
    ip = 0
    out = []
    while ip < len(program):
        if debug:
            "-------"
            print(f"{a=},{b=},{c=},{ip=},{out=}")
        op, x = program[ip], program[ip + 1]
        if op == 0:  # adv
            a = a // (2 ** combo(x, a, b, c))
            ip += 2
        elif op == 1:  # bxl
            b ^= x
            ip += 2
        elif op == 2:  # bst
            b = combo(x, a, b, c) % 8
            ip += 2
        elif op == 3:  # jnz
            if a != 0:
                ip = x
            else:
                ip += 2
        elif op == 4:  # bxc
            b ^= c
            ip += 2
        elif op == 5:  # out
            out.append(combo(x, a, b, c) % 8)
            ip += 2
        elif op == 6:  # bdv
            b = a // 2 ** combo(x, a, b, c)
            ip += 2
        elif op == 7:  # cdv
            c = a // 2 ** combo(x, a, b, c)
            ip += 2
        else:
            raise RuntimeError("invalid opcode")
        if debug:
            print(opname[op], x)
            print(f"{a=},{b=},{c=},{ip=},{out=}")
            input()

    return out


def solve(lines: list[str]) -> tuple[str, int]:
    a = int(lines[0].removeprefix("Register A: "))
    b = int(lines[1].removeprefix("Register B: "))
    c = int(lines[2].removeprefix("Register C: "))
    program = [int(c) for c in lines[4].removeprefix("Program: ").split(",")]
    out = execute(program, a, b, c, debug=False)
    part_one = ",".join(str(s) for s in out)
    to_try = list((i, 1) for i in range(8))
    solutions = []
    while to_try:
        a, n = to_try.pop()
        out = execute(program, a, b, c)
        if out == program[-1 * n :]:
            if len(out) == len(program):
                solutions.append(a)
            else:
                to_try += [(8 * a + i, len(out) + 1) for i in range(8)]

    return part_one, min(solutions)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
