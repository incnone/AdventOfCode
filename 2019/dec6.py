from collections import defaultdict


def get_total_num_orbits(orbits):
    orbiters = defaultdict(lambda: set())
    for satellite, obj in orbits.items():
        orbiters[obj].add(satellite)
    depths = dict()

    def fill_depths(base_obj, depth):
        depths[base_obj] = depth
        for sat in orbiters[base_obj]:
            fill_depths(sat, depth+1)

    fill_depths('COM', 0)

    num_orbits = 0
    for depth in depths.values():
        num_orbits += depth

    return num_orbits


def get_path_to_com(object, orbits):
    path = [object]
    next_object = object
    while next_object != 'COM':
        next_object = orbits[next_object]
        path.append(next_object)
    return path


def get_shortest_path_length(obj_1, obj_2, orbits):
    obj_1_to_com = get_path_to_com(obj_1, orbits)
    obj_2_to_com = get_path_to_com(obj_2, orbits)

    split_idx = 0
    for iter1, iter2 in zip(reversed(obj_1_to_com), reversed(obj_2_to_com)):
        if iter1 != iter2:
            break
        split_idx += 1

    return len(obj_2_to_com) + len(obj_1_to_com) - 2*split_idx


if __name__ == "__main__":
    orbits = dict()

    with open('input/dec6.txt', 'r') as file:
        for line in file:
            objs = line.split(')')
            orbits[objs[1].rstrip('\n')] = objs[0]

    print(get_total_num_orbits(orbits=orbits))
    print(get_shortest_path_length('YOU', 'SAN', orbits) - 2)
