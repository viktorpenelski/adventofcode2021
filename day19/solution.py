from dataclasses import dataclass
from math import sqrt
from typing import List, Dict, Tuple, Optional, Callable
import re


@dataclass
class Point3d:
    x: int
    y: int
    z: int

    def distance_to(self, pt: 'Point3d') -> float:
        return sqrt(pow(pt.x - self.x, 2) + pow(pt.y - self.y, 2) + pow(pt.z - self.z, 2))

    def manhattan_distance_to(self, pt: 'Point3d') -> int:
        return self.x - pt.x + self.y - pt.y + self.z - pt.z

    def __eq__(self, other: 'Point3d') -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return self.x * self.y * self.z

    def __sub__(self, other: 'Point3d') -> 'Point3d':
        return Point3d(self.x-other.x, self.y-other.y, self.z-other.z)

    def __add__(self, other: 'Point3d') -> 'Point3d':
        return Point3d(self.x+other.x, self.y+other.y, self.z+other.z)


orientations = [
    lambda pt: Point3d(pt.x, pt.y, pt.z),
    lambda pt: Point3d(pt.y, pt.z, pt.x),
    lambda pt: Point3d(pt.z, pt.x, pt.y),
    lambda pt: Point3d(pt.z, pt.y, -pt.x),
    lambda pt: Point3d(pt.y, pt.x, -pt.z),
    lambda pt: Point3d(pt.x, pt.z, -pt.y),
    lambda pt: Point3d(pt.x, -pt.y, -pt.z),
    lambda pt: Point3d(pt.y, -pt.z, -pt.x),
    lambda pt: Point3d(pt.z, -pt.x, -pt.y),
    lambda pt: Point3d(pt.z, -pt.y, pt.x),
    lambda pt: Point3d(pt.y, -pt.x, pt.z),
    lambda pt: Point3d(pt.x, -pt.z, pt.y),
    lambda pt: Point3d(-pt.x, pt.y, -pt.z),
    lambda pt: Point3d(-pt.y, pt.z, -pt.x),
    lambda pt: Point3d(-pt.z, pt.x, -pt.y),
    lambda pt: Point3d(-pt.z, pt.y, pt.x),
    lambda pt: Point3d(-pt.y, pt.x, pt.z),
    lambda pt: Point3d(-pt.x, pt.z, pt.y),
    lambda pt: Point3d(-pt.x, -pt.y, pt.z),
    lambda pt: Point3d(-pt.y, -pt.z, pt.x),
    lambda pt: Point3d(-pt.z, -pt.x, pt.y),
    lambda pt: Point3d(-pt.z, -pt.y, -pt.x),
    lambda pt: Point3d(-pt.y, -pt.x, -pt.z),
    lambda pt: Point3d(-pt.x, -pt.z, -pt.y),
]


class Scanner:
    id: int
    beacons: List[Point3d]
    pos: Optional[Point3d] = None
    distance_map: Dict[float, Tuple[int, int]]

    def __init__(self, id: int, beacons: List[Point3d], pos: Optional[Point3d] = None):
        self.id = id
        self.beacons = beacons
        self.pos = pos
        self.distance_map = self._calculate_distances_map(beacons)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

    def __str__(self):
        return f'<{self.id} @ {self.pos}>'

    @staticmethod
    def _calculate_distances_map(beacons: List[Point3d]):
        distances = {}
        for b_idx_1 in range(0, len(beacons)):
            for b_idx_2 in range(b_idx_1 + 1, len(beacons)):
                distances[beacons[b_idx_1].distance_to(beacons[b_idx_2])] = (b_idx_1, b_idx_2)
        return distances

    def rotate_and_offset(self, rotation: Callable[[Point3d], Point3d], offset: Point3d):
        return Scanner(self.id, [rotation(b) + offset for b in self.beacons], pos=offset)


def parse_inputs():
    with open('in.txt') as f:
        lines = f.readlines()
        scanners = []
        last_id = -1
        beacons = []
        for line in lines:
            new_scanner = re.match('--- scanner (\\d+) ---', line)
            if new_scanner:
                # sc = Scanner(int(new_scanner.group(1)), [])
                # scanners.append(sc)
                last_id = new_scanner.group(1)
                continue
            elif line.strip() == '':
                scanners.append(Scanner(last_id, beacons))
                beacons = []
                continue
            split = line.split(',')
            pt = Point3d(int(split[0]), int(split[1]), int(split[2]))
            beacons.append(pt)
        scanners.append(Scanner(last_id, beacons))
    return scanners


def try_fix_scanner(sc: Scanner, correctly_aligned_scanners: List[Scanner]) -> Optional[Scanner]:
    for sc_correct in correctly_aligned_scanners:
        overlap = set(sc.distance_map.keys()).intersection(set(sc_correct.distance_map.keys()))
        # 66 is 11+10+...+1 (all combinations of matching distances between 12 pts)
        if len(overlap) < 66:
            continue
        for distance in overlap:
            # get the two beacons from both scanners where distances are matching
            idx_b1, idx_b2 = sc.distance_map[distance]
            idx_fixed_b1, idx_fixed_b2 = sc_correct.distance_map[distance]
            for orientation in orientations:
                # 1. rotate both beacons that we are trying to allign for each possible orientation
                rotated_b1 = orientation(sc.beacons[idx_b1])
                rotated_b2 = orientation(sc.beacons[idx_b2])
                # 2.1 we have a potential fix!
                if rotated_b1 - sc_correct.beacons[idx_fixed_b1] == rotated_b2 - sc_correct.beacons[idx_fixed_b2]:
                    # offset is "proper" beacon minus the correctly aligned beacon
                    offset = sc_correct.beacons[idx_fixed_b1] - rotated_b1
                    # transform all beacons for the given scanner
                    fixed_sc = sc.rotate_and_offset(orientation, offset)
                    intersecting_beacons = len(set(fixed_sc.beacons) & set(sc_correct.beacons))
                    # Sanity check that we now have at least 12 "same" beacons in both scanners
                    if intersecting_beacons >= 12:
                        return fixed_sc
                # 2.2 same as 2.1, but assume points b1 and b2 are flipped
                if rotated_b2 - sc_correct.beacons[idx_fixed_b1] == rotated_b1 - sc_correct.beacons[idx_fixed_b2]:
                    offset = sc_correct.beacons[idx_fixed_b2] - rotated_b1
                    fixed_sc = sc.rotate_and_offset(orientation, offset)
                    if len(set(fixed_sc.beacons) & set(sc_correct.beacons)) >= 12:
                        return fixed_sc
    return None


all_scanners = parse_inputs()
all_scanners[0].pos = Point3d(0, 0, 0)  # assume orientation of the first scanner as base
to_be_fixed = all_scanners[1:]  # consider all other scanners "unaligned"
fixed_scanners = [all_scanners[0]]  # consider first scanner "aligned"
while len(fixed_scanners) < len(all_scanners):
    fixed = None
    scanner = None
    for sc in to_be_fixed:
        fixed = try_fix_scanner(sc, fixed_scanners)
        if fixed:
            fixed_scanners.append(fixed)
            to_be_fixed.remove(sc)
            break

all_beacons = set()
for scanner in fixed_scanners:
    all_beacons.update(scanner.beacons)
print(len(all_beacons))

max_dist = 0
for s1 in fixed_scanners:
    for s2 in fixed_scanners:
        dist = s1.pos.manhattan_distance_to(s2.pos)
        if dist > max_dist:
            max_dist = dist
print(max_dist)
