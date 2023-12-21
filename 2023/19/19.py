import re
import sys
from operator import gt, lt
from time import perf_counter
from typing import Callable

DIGIT_PATTERN = re.compile(r"\d+")
OPERATOR_MAP = {">": gt, "<": lt}

Part = dict[str, int]
Workflow = list[Callable[[dict[str, int]], str]]


def make_const_fn(return_value: str) -> Callable[[Part], str]:
    def fn(x: Part) -> str:
        return return_value

    return fn


def make_conditional_fn(
    return_value: str, key: str, num: int, op_str: str
) -> Callable[[Part], str]:
    def fn(x: Part) -> str:
        return return_value if OPERATOR_MAP[op_str](x[key], num) else ""

    return fn


def get_workflow(line: str) -> tuple[str, Workflow]:
    workflow = []
    name, rule_str = line.split("{")
    rule_list = rule_str[:-1].split(",")
    for rule in rule_list:
        rule = rule.split(":")
        if len(rule) == 1:
            workflow.append(make_const_fn(rule[0]))
            continue
        rule, next_label = rule
        key = rule[0]
        num = int(rule[2:])
        workflow.append(make_conditional_fn(next_label, key, num, rule[1]))

    return name, workflow


def call_workflow(workflow: Workflow, part: Part) -> str:
    for rule in workflow:
        result = rule(part)
        if result:
            return result
    raise ValueError("No result!")


def get_part(line: str) -> Part:
    part = {}
    for char, result in zip("xmas", DIGIT_PATTERN.findall(line)):
        part[char] = int(result)
    return part


def accept_part(workflows: dict[str, Workflow], part: Part) -> bool:
    result = "in"
    workflow = workflows[result]
    while True:
        result = call_workflow(workflow, part)
        if result == "A":
            return True
        elif result == "R":
            return False
        workflow = workflows[result]


def solve(lines: list[str]) -> tuple[int, int]:
    workflows = {}
    parts = []
    parsing = "workflows"
    for line in lines:
        if line == "":
            parsing = "rules"
            continue
        if parsing == "workflows":
            name, workflow = get_workflow(line)
            workflows[name] = workflow
        else:
            parts.append(get_part(line))

    sum_accepted = 0
    for part in parts:
        accept = accept_part(workflows, part)
        if accept:
            sum_accepted += sum(part.values())
    return sum_accepted, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    sum_accepted, possible_accepted = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{sum_accepted=}, {possible_accepted=} ({time_us}µs)")
