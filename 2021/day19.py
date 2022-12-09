import textwrap
import re
import numpy as np
import itertools
from collections import defaultdict


def get_test_input() -> str:
    return textwrap.dedent("""\
    --- scanner 0 ---
    404,-588,-901
    528,-643,409
    -838,591,734
    390,-675,-793
    -537,-823,-458
    -485,-357,347
    -345,-311,381
    -661,-816,-575
    -876,649,763
    -618,-824,-621
    553,345,-567
    474,580,667
    -447,-329,318
    -584,868,-557
    544,-627,-890
    564,392,-477
    455,729,728
    -892,524,684
    -689,845,-530
    423,-701,434
    7,-33,-71
    630,319,-379
    443,580,662
    -789,900,-551
    459,-707,401
    
    --- scanner 1 ---
    686,422,578
    605,423,415
    515,917,-361
    -336,658,858
    95,138,22
    -476,619,847
    -340,-569,-846
    567,-361,727
    -460,603,-452
    669,-402,600
    729,430,532
    -500,-761,534
    -322,571,750
    -466,-666,-811
    -429,-592,574
    -355,545,-477
    703,-491,-529
    -328,-685,520
    413,935,-424
    -391,539,-444
    586,-435,557
    -364,-763,-893
    807,-499,-711
    755,-354,-619
    553,889,-390
    
    --- scanner 2 ---
    649,640,665
    682,-795,504
    -784,533,-524
    -644,584,-595
    -588,-843,648
    -30,6,44
    -674,560,763
    500,723,-460
    609,671,-379
    -555,-800,653
    -675,-892,-343
    697,-426,-610
    578,704,681
    493,664,-388
    -671,-858,530
    -667,343,800
    571,-461,-707
    -138,-166,112
    -889,563,-600
    646,-828,498
    640,759,510
    -630,509,768
    -681,-892,-333
    673,-379,-804
    -742,-814,-386
    577,-820,562
    
    --- scanner 3 ---
    -589,542,597
    605,-692,669
    -500,565,-823
    -660,373,557
    -458,-679,-417
    -488,449,543
    -626,468,-788
    338,-750,-386
    528,-832,-391
    562,-778,733
    -938,-730,414
    543,643,-506
    -524,371,-870
    407,773,750
    -104,29,83
    378,-903,-323
    -778,-728,485
    426,699,580
    -438,-605,-362
    -469,-447,-387
    509,732,623
    647,635,-688
    -868,-804,481
    614,-800,639
    595,780,-596
    
    --- scanner 4 ---
    727,592,562
    -293,-554,779
    441,611,-461
    -714,465,-776
    -743,427,-804
    -660,-479,-426
    832,-632,460
    927,-485,-438
    408,393,-506
    466,436,-512
    110,16,151
    -258,-428,682
    -393,719,612
    -211,-452,876
    808,-476,-593
    -575,615,604
    -485,667,467
    -680,325,-822
    -627,-443,-432
    872,-547,-609
    833,512,582
    807,604,487
    839,-516,451
    891,-625,532
    -652,-548,-490
    30,-46,-14""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    scanner_number = None
    scanner_re = re.compile(r'--- scanner (?P<n>\d+) ---')
    data = defaultdict(lambda: list())
    for line in s.splitlines(keepends=False):
        if not line:
            continue

        m = scanner_re.match(line)
        if m is not None:
            scanner_number = int(m.groupdict()['n'])
        elif scanner_number is not None:
            data[scanner_number].append(np.array(list(int(x) for x in line.split(','))))  # row vector
        else:
            assert False

    return data


fix_x_transforms = [
    np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]),
    np.array([
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ]),
    np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1]
    ]),
    np.array([
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0]
    ])
]
move_x_transforms = [
    np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]),
    np.array([
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 1]
    ]),
    np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ]),
    np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ]),
    np.array([
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ]),
    np.array([
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0]
    ]),
]
all_transforms = [np.dot(x, y) for x in fix_x_transforms for y in move_x_transforms]
assert len(all_transforms) == 24


def num_agreements(s1, s2):     # s1, s2 are sorted lists of DISTINCT tuples
    ans = 0
    i = 0
    j = 0
    while i < len(s1) and j < len(s2):
        if s1[i] == s2[j]:
            ans += 1
        i, j = i + (s1[i] <= s2[j]), j + (s2[j] <= s1[i])
    return ans


def find_match(s_unfixed, s_fixed, n=12):
    """
    s1, s2 are lists of row vectors. returns (R, B) such that the map x |-> xR + B, applied to s_unfixed,
    causes s_unfixed to intersect s_fixed in at least n spots
    """

    for x, y, r in itertools.product(s_unfixed, s_fixed, all_transforms):
        b = y - (x @ r)
        transformed_pts = sorted(tuple(x @ r + b) for x in s_unfixed)
        k = num_agreements(s_fixed, transformed_pts)
        if k >= n:
            return r, b

    return None


def part_1(data):
    # location, rotation; for (R, B), the "real" scanner data is at xR + B (for detected beacon at x)
    fixed_scanner_indices = [0]
    fixed_scanners = {0: (np.array([[0], [0], [0]]), np.identity(3))}
    fixed_scanner_data = {0: sorted(tuple(x) for x in data[0])}   # sorted tuples
    unfixed_scanners = list(range(1, len(data)))
    idx = 0
    while idx < len(fixed_scanner_indices):
        s_fixed = fixed_scanner_indices[idx]
        matched_scanners = []
        for s_unfixed in unfixed_scanners:
            print(f'Finding match between {s_unfixed} and {s_fixed}...', end=" ")
            match = find_match(data[s_unfixed], fixed_scanner_data[s_fixed])
            if match is not None:
                fixed_scanner_indices.append(s_unfixed)
                fixed_scanners[s_unfixed] = match
                match_r, match_b = match
                fixed_scanner_data[s_unfixed] = sorted(tuple((x @ match_r) + match_b) for x in data[s_unfixed])
                matched_scanners.append(s_unfixed)
                fixed_any = True
                print(f'Found! Scanner {s_unfixed} is at {match_b}.')
            else:
                print('None found.')
        unfixed_scanners = [x for x in unfixed_scanners if x not in matched_scanners]
        idx += 1

    all_beacons = set()
    for d in fixed_scanner_data.values():
        all_beacons = all_beacons.union(d)

    with open('day19b.txt', 'w') as file:
        for s, p in fixed_scanners.items():
            file.write(f'{s}: {p[0]}, {p[1]}')

    print(f'Part 1: {len(all_beacons)}')


def part_2(data):
    regex = re.compile(r'Scanner (?P<n>\d+) is at \[\s*(?P<x>-?\d+)\s+(?P<y>-?\d+)\s+(?P<z>-?\d+)]')
    #regex = re.compile(r'(?P<n>\d+): \[ (?P<x>-?\d+) (?P<y>-?\d+) (?P<z>-?\d+)]')
    scanners = [(0, 0, 0, 0)]
    with open('input/day19b.txt', 'r') as file:
        for line in file:
            m = regex.search(line)
            if m is not None:
                g = m.groupdict()
                scanners.append((int(g['n']), int(g['x']), int(g['y']), int(g['z'])))

    assert len(scanners) == 30

    def dist_taxi(t1, t2):
        return sum(abs(t1[i] - t2[i]) for i in range(len(t1)))

    ans = max(dist_taxi(s1[1:], s2[1:]) for s1, s2 in itertools.combinations(scanners, 2))
    print(f'Part 2: {ans}')


def main():
    data = read_input(day_number=19, test=False)

    # for k, v in data.items():
    #     print(f'--- scanner {k} ---')
    #     for sc in v:
    #         print(str(sc))

    #part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
