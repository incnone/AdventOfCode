import textwrap
import queue
import itertools
from typing import Dict, List, Tuple, Optional

"""\
#############
#01.2.3.4.56#
###7#8#9#A###       depth = 0
  #B#C#D#E#         depth = 1
  #########"""

room_depth = 4
paths = {
    (0, 7): [1],
    (1, 7): [],
    (2, 7): [],
    (3, 7): [2],
    (4, 7): [2, 3],
    (5, 7): [2, 3, 4],
    (6, 7): [2, 3, 4, 5],

    (0, 8): [1, 2],
    (1, 8): [2],
    (2, 8): [],
    (3, 8): [],
    (4, 8): [3],
    (5, 8): [3, 4],
    (6, 8): [3, 4, 5],

    (0, 9): [1, 2, 3],
    (1, 9): [2, 3],
    (2, 9): [3],
    (3, 9): [],
    (4, 9): [],
    (5, 9): [4],
    (6, 9): [4, 5],

    (0, 10): [1, 2, 3, 4],
    (1, 10): [2, 3, 4],
    (2, 10): [3, 4],
    (3, 10): [4],
    (4, 10): [],
    (5, 10): [],
    (6, 10): [5],

    (7, 8): [2],
    (7, 9): [2, 3],
    (7, 10): [2, 3, 4],

    (8, 7): [2],
    (8, 9): [3],
    (8, 10): [3, 4],

    (9, 7): [3, 2],
    (9, 8): [3],
    (9, 10): [4],

    (10, 7): [4, 3, 2],
    (10, 8): [4, 3],
    (10, 9): [4],
}
path_lens = {
    (0, 7): 3,
    (1, 7): 2,
    (2, 7): 2,
    (3, 7): 4,
    (4, 7): 6,
    (5, 7): 8,
    (6, 7): 9,

    (0, 8): 5,
    (1, 8): 4,
    (2, 8): 2,
    (3, 8): 2,
    (4, 8): 4,
    (5, 8): 6,
    (6, 8): 7,

    (0, 9): 7,
    (1, 9): 6,
    (2, 9): 4,
    (3, 9): 2,
    (4, 9): 2,
    (5, 9): 4,
    (6, 9): 5,

    (0, 10): 9,
    (1, 10): 8,
    (2, 10): 6,
    (3, 10): 4,
    (4, 10): 2,
    (5, 10): 2,
    (6, 10): 3,

    (7, 8): 4,
    (7, 9): 6,
    (7, 10): 8,

    (8, 7): 4,
    (8, 9): 4,
    (8, 10): 6,

    (9, 7): 6,
    (9, 8): 4,
    (9, 10): 4,

    (10, 7): 8,
    (10, 8): 6,
    (10, 9): 4,
}


def in_hall(idx: int) -> bool:
    return idx < 7


def in_room(idx: int) -> bool:
    return not in_hall(idx)


def room_indices(room: int) -> List[int]:
    indices = [room+7]
    for _ in range(1, room_depth):
        indices += [indices[-1] + 4]
    return indices


def get_room_for_index(idx: int) -> Optional[int]:
    if idx < 7:
        return None
    return (idx - 7) % 4


def get_depth_for_index(idx: int) -> Optional[int]:
    if idx < 7:
        return None
    return (idx - 7) // 4


def get_room_index(room: int, depth: int) -> int:
    return 7 + 4*depth + room


def add_extra_into_room_paths():
    base_paths = paths.copy()
    for k, v in base_paths.items():
        if 7 <= k[1] <= 10:
            room = get_room_for_index(k[1])
            for depth in range(1, room_depth):
                paths[(k[0], get_room_index(room, depth))] = v + room_indices(room)[:depth]
                path_lens[(k[0], get_room_index(room, depth))] = path_lens[(k[0], get_room_index(room, 0))] + depth


def add_flipped_paths():
    base_paths = paths.copy()
    for k, v in base_paths.items():
        paths[(k[1], k[0])] = list(reversed(v))
        path_lens[(k[1], k[0])] = path_lens[k]


def make_paths():
    global paths
    global path_lens

    add_extra_into_room_paths()
    add_flipped_paths()
    add_extra_into_room_paths()
    add_flipped_paths()

    base_paths = paths.copy()
    for k, v in base_paths.items():
        paths[k] = v + [k[1]]


def get_end_pos():
    return tuple([0]*7 + [1, 2, 3, 4]*room_depth)


def get_test_input() -> str:
    if room_depth == 2:
        return textwrap.dedent("""\
        #############
        #...........#
        ###B#C#B#D###
          #A#D#C#A#
          #########""")
    elif room_depth == 4:
        return textwrap.dedent("""\
        #############
        #...........#
        ###B#C#B#D###
          #D#C#B#A#
          #D#B#A#C#
          #A#D#C#A#
          #########""")
    else:
        assert False


def get_critical_positions():
    if room_depth == 2:
        str_pos = [
            textwrap.dedent("""\
            #############
            #...B.......#
            ###B#C#.#D###
              #A#D#C#A#
              #########"""),

            textwrap.dedent("""\
            #############
            #...B.......#
            ###B#.#C#D###
              #A#D#C#A#
              #########"""),

            textwrap.dedent("""\
            #############
            #.....D.....#
            ###B#.#C#D###
              #A#B#C#A#
              #########"""),

            textwrap.dedent("""\
            #############
            #.....D.....#
            ###.#B#C#D###
              #A#B#C#A#
              #########"""),

            textwrap.dedent("""\
            #############
            #.....D.D.A.#
            ###.#B#C#.###
              #A#B#C#.#
              #########"""),

            textwrap.dedent("""\
            #############
            #.........A.#
            ###.#B#C#D###
              #A#B#C#D#
              #########"""),

            textwrap.dedent("""\
            #############
            #...........#
            ###A#B#C#D###
              #A#B#C#D#
              #########"""),
        ]
    elif room_depth == 4:
        str_pos = [
            textwrap.dedent("""\
                #############
                #...........#
                ###B#C#B#D###
                  #D#C#B#A#
                  #D#B#A#C#
                  #A#D#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #..........D#
                ###B#C#B#.###
                  #D#C#B#A#
                  #D#B#A#C#
                  #A#D#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #A.........D#
                ###B#C#B#.###
                  #D#C#B#.#
                  #D#B#A#C#
                  #A#D#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #A........BD#
                ###B#C#.#.###
                  #D#C#B#.#
                  #D#B#A#C#
                  #A#D#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #A......B.BD#
                ###B#C#.#.###
                  #D#C#.#.#
                  #D#B#A#C#
                  #A#D#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.....B.BD#
                ###B#C#.#.###
                  #D#C#.#.#
                  #D#B#.#C#
                  #A#D#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.....B.BD#
                ###B#.#.#.###
                  #D#C#.#.#
                  #D#B#C#C#
                  #A#D#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.....B.BD#
                ###B#.#.#.###
                  #D#.#C#.#
                  #D#B#C#C#
                  #A#D#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA...B.B.BD#
                ###B#.#.#.###
                  #D#.#C#.#
                  #D#.#C#C#
                  #A#D#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.D.B.B.BD#
                ###B#.#.#.###
                  #D#.#C#.#
                  #D#.#C#C#
                  #A#.#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.D...B.BD#
                ###B#.#.#.###
                  #D#.#C#.#
                  #D#.#C#C#
                  #A#B#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.D.....BD#
                ###B#.#.#.###
                  #D#.#C#.#
                  #D#B#C#C#
                  #A#B#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.D......D#
                ###B#.#.#.###
                  #D#B#C#.#
                  #D#B#C#C#
                  #A#B#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.D......D#
                ###B#.#C#.###
                  #D#B#C#.#
                  #D#B#C#.#
                  #A#B#C#A#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.D.....AD#
                ###B#.#C#.###
                  #D#B#C#.#
                  #D#B#C#.#
                  #A#B#C#.#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.......AD#
                ###B#.#C#.###
                  #D#B#C#.#
                  #D#B#C#.#
                  #A#B#C#D#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.......AD#
                ###.#B#C#.###
                  #D#B#C#.#
                  #D#B#C#.#
                  #A#B#C#D#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.......AD#
                ###.#B#C#.###
                  #.#B#C#.#
                  #D#B#C#D#
                  #A#B#C#D#
                  #########"""),

            textwrap.dedent("""\
                #############
                #AA.......AD#
                ###.#B#C#.###
                  #.#B#C#D#
                  #.#B#C#D#
                  #A#B#C#D#
                  #########"""),

            textwrap.dedent("""\
                #############
                #A........AD#
                ###.#B#C#.###
                  #.#B#C#D#
                  #A#B#C#D#
                  #A#B#C#D#
                  #########"""),

            textwrap.dedent("""\
                #############
                #.........AD#
                ###.#B#C#.###
                  #A#B#C#D#
                  #A#B#C#D#
                  #A#B#C#D#
                  #########"""),

            textwrap.dedent("""\
                #############
                #..........D#
                ###A#B#C#.###
                  #A#B#C#D#
                  #A#B#C#D#
                  #A#B#C#D#
                  #########"""),

            textwrap.dedent("""\
                #############
                #...........#
                ###A#B#C#D###
                  #A#B#C#D#
                  #A#B#C#D#
                  #A#B#C#D#
                  #########"""),
        ]

    else:
        assert False

    return [parse_position(s) for s in str_pos]


def read_input(day_number, test=False):
    if test:
        return parse_position(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_position(file.read())


def parse_position(s: str):
    vals = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, '.': 0
    }
    lines = s.splitlines(keepends=False)
    row0 = map(lambda x: vals[x], lines[1][1:3] + lines[1][4:9:2] + lines[1][10:12])
    rooms = []
    for depth in range(room_depth):
        rooms.append(list(map(lambda x: vals[x], lines[2+depth][3:10:2])))

    vals_list = list(row0) + list(itertools.chain.from_iterable(rooms))
    return tuple(
        vals_list
    )


def path_exists(pos: tuple, idx: int, room_idx: int):
    return all([pos[j] == 0 for j in paths[(idx, room_idx)]])


def get_str(pos: tuple):
    vals = {
        0: '.', 1: 'A', 2: 'B', 3: 'C', 4: 'D'
    }
    c = [vals[x] for x in pos]

    if room_depth == 2:
        return textwrap.dedent(f"""\
        #############
        #{c[0]}{c[1]}.{c[2]}.{c[3]}.{c[4]}.{c[5]}{c[6]}#
        ###{c[7]}#{c[8]}#{c[9]}#{c[10]}###
          #{c[11]}#{c[12]}#{c[13]}#{c[14]}#
          #########""")

    elif room_depth == 4:
        return textwrap.dedent(f"""\
        #############
        #{c[0]}{c[1]}.{c[2]}.{c[3]}.{c[4]}.{c[5]}{c[6]}#
        ###{c[7]}#{c[8]}#{c[9]}#{c[10]}###
          #{c[11]}#{c[12]}#{c[13]}#{c[14]}#
          #{c[15]}#{c[16]}#{c[17]}#{c[18]}#
          #{c[19]}#{c[20]}#{c[21]}#{c[22]}#
          #########""")


def cpm(val: int) -> int:
    return 10**(val-1)


def get_minimal_cost(pos) -> int:
    """Gets a heuristic cost for moving pos to end_pos"""

    cost = 0
    num_to_move = dict()
    for room in range(4):
        n = 0
        for d in range(room_depth-1, -1, -1):
            if pos[get_room_index(room, d)] != room+1:
                break
            n += 1
        num_to_move[room] = room_depth - n

    print(num_to_move)
    for room in range(4):
        for d in range(0, num_to_move[room]):
            val = pos[get_room_index(room, d)]
            # cost to move this value out of this room and to the tile above its destination
            cost += ((d+1) + 2*abs(room - (val-1)))*cpm(val)

        # cost to move the things that belong in this room from the tile above it down into the room
        cost += (((num_to_move[room]+1)*(num_to_move[room]))//2)*cpm(room+1)

    return cost


def get_cost(val, src_idx, dest_idx) -> int:
    """Gets a reduced A* cost: The cost of making the move that is in excess of the "required" or "heuristic" cost
    (the latter meaning the cost due to magically moving stuff to its destination without concern for collisions).
    Assumes that if src_idx is in the hall, then dest_idx is in a room and the cost is zero."""
    if in_room(dest_idx):
        return 0

    # If here, then src_idx is our starting room, and dest_idx is in the hall. We need to know how many extra spaces
    # in the hall we will have to move as a result of moving here.
    index_hall_locs = {
        0: 0,
        1: 1,
        2: 3,
        3: 5,
        4: 7,
        5: 9,
        6: 10
    }
    room_hall_locs = {
        0: 2,
        1: 4,
        2: 6,
        3: 8
    }
    hall_idx = index_hall_locs[dest_idx]
    src_room_idx = room_hall_locs[get_room_for_index(src_idx)]
    dest_room_idx = room_hall_locs[val - 1]

    return cpm(val) * (abs(src_room_idx - hall_idx) + abs(dest_room_idx - hall_idx) - abs(src_room_idx - dest_room_idx))


def get_legal_moves(pos: tuple):
    legal_moves = []
    for idx, val in enumerate(pos):
        if val == 0:
            continue

        # If we aren't in our room, check whether we can move into our room
        room = val-1
        current_room = get_room_for_index(idx)
        if current_room != room:
            current_depth = room_depth-1
            incorrect_occupant = False

            # Counting from the back, we need all full spots to be correctly full, and one spot empty
            while current_depth >= 0:
                val_at_move = pos[get_room_index(room=room, depth=current_depth)]
                if val_at_move == 0:
                    break
                elif val_at_move != val:
                    incorrect_occupant = True
                    break
                current_depth -= 1

            # In this case, we can move into the room at spot `move_into_index`
            if not incorrect_occupant and current_depth >= 0:
                move_into_index = get_room_index(room=room, depth=current_depth)
                if path_exists(pos, idx, move_into_index):
                    new_move = list(pos)
                    new_move[idx] = 0
                    new_move[move_into_index] = val

                    # If we were in a room, and we can move to our room, then we need consider no other moves
                    if in_room(idx):
                        return [(tuple(new_move), 0)]
                    else:
                        legal_moves.append((tuple(new_move), get_cost(val, idx, move_into_index)))

        # If we're in our destination and everyone behind us is also, don't move
        else:
            our_depth = get_depth_for_index(idx)
            if all([get_room_index(current_room, d) == val for d in range(our_depth+1, room_depth)]):
                continue

        # If we're in a room, check whether we can move into the hallway
        if current_room is not None:
            for dest_idx in range(0, 7):
                if path_exists(pos, idx, dest_idx):
                    new_move = list(pos)
                    new_move[idx] = 0
                    new_move[dest_idx] = val
                    legal_moves.append((tuple(new_move), get_cost(val, idx, dest_idx)))

    return legal_moves


def part_1(data):
    debug_pos = parse_position(textwrap.dedent("""\
        #############
        #A........AD#
        ###.#B#C#.###
          #.#B#C#D#
          #A#B#C#D#
          #A#B#C#D#
          #########"""),)

    mincost = get_minimal_cost(data)
    end_pos = get_end_pos()
    critical_positions = get_critical_positions()

    print(data)
    pq = queue.PriorityQueue()
    pq.put_nowait((0, data, 0))
    distances = {data: 0}
    prevnodes = dict()
    maxdepth = -1
    numloops = 0

    while not pq.empty():
        numloops += 1
        dist, pos, depth = pq.get_nowait()
        # if pos in critical_positions:
        #     print(f'Found a critical position at distance {dist}:')
        #     print(get_str(pos))

        if pos == end_pos:
            print('Found the end position!')
            break

        if distances[pos] < dist:
            continue

        # if depth > maxdepth:
        #     maxdepth = depth
        #     print(f'Reached a depth of {depth}, queue has length {pq.qsize()}')
        #     if depth == 32:
        #         with open('data/depth32.txt', 'w') as file:
        #             file.write('-----Depth 32 position--------\n')
        #             file.write(get_str(pos))
        #
        #             prevpos = pos
        #             while prevpos in prevnodes:
        #                 prevpos = prevnodes[prevpos]
        #                 file.write('\n---\n')
        #                 file.write(get_str(prevpos))

        # if numloops % 10000 == 0:
        #     print(f'Numloops is {numloops}')

        moves = get_legal_moves(pos)
        for next_pos, cost in moves:
            if next_pos not in distances or (dist+cost) < distances[next_pos]:
                distances[next_pos] = dist+cost
                prevnodes[next_pos] = pos
                pq.put_nowait((dist+cost, next_pos, depth+1))

    print(mincost, distances[end_pos])
    print(f'Part 1: {distances[end_pos] + mincost}')

    currpos = end_pos
    soln_path = [(end_pos, distances[end_pos])]
    while currpos != data and currpos in prevnodes:
        currpos = prevnodes[currpos]
        soln_path.append((currpos, distances[currpos]))

    soln_path = reversed(soln_path)
    with open('day23soln.txt', 'w') as file:
        idx = 0
        for p, d in soln_path:
            file.write(f'Move {idx} at distance {d}:')
            file.write(get_str(p))
            file.write('\n')
            idx += 1


def part_2(data):
    pass


def main():
    make_paths()

    with open('data/day_23_paths.txt', 'w') as file:
        for k, v in paths.items():
            file.write(f'{k}: {v}\n')

    data = read_input(day_number=23, test=False)
    part_1(data)
    #part_2(data)


if __name__ == "__main__":
    main()
