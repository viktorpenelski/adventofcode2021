from dataclasses import dataclass, field
from typing import Set, Dict


@dataclass
class CaveNode:
    name: str
    connections: Set['CaveNode'] = field(default_factory=set)

    def is_small(self):
        return self.name.islower()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()


def parse_input() -> Dict[str, CaveNode]:
    caves: Dict[str, CaveNode] = {}
    with open('in.txt') as f:
        for line in f.readlines():
            first_cave_name, second_cave_name = line.strip().split('-')
            if not first_cave_name in caves:
                caves[first_cave_name] = CaveNode(first_cave_name)
            if not second_cave_name in caves:
                caves[second_cave_name] = CaveNode(second_cave_name)
            caves[first_cave_name].connections.add(caves[second_cave_name])
            caves[second_cave_name].connections.add(caves[first_cave_name])

    return caves


def traverse(cave: CaveNode, caves: Dict[str, CaveNode], visited: Set[str], small_pass=False):
    if cave.name == 'end':
        return 1
    if cave.name in visited and cave.is_small() and small_pass and cave.name != 'start':
        small_pass = False
    elif cave.name in visited and cave.is_small():
        return 0

    visited.add(cave.name)
    paths = 0
    for connection in cave.connections:
        paths += traverse(connection, caves, visited.copy(), small_pass)
    return paths


caves = parse_input()
print(traverse(caves['start'], caves, set()))
print(traverse(caves['start'], caves, set(), True))
