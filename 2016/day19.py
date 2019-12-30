from getinput import get_input


def part_1(num_elves):
    elves = [True]*num_elves
    cursor = -1
    elves_remaining = num_elves - 1
    skipped = False
    while elves_remaining:
        cursor = (cursor + 1) % num_elves
        if not elves[cursor]:
            continue

        if not skipped:
            skipped = True
        else:
            skipped = False
            elves[cursor] = False
            elves_remaining -= 1

    return elves.index(True) + 1


def part_2(num_elves):
    last_winner = 0
    last_num_elves = 1
    while last_num_elves < num_elves:
        last_num_elves += 1
        if last_winner < last_num_elves//2 - 1:
            last_winner = (last_winner + 1) % last_num_elves
        else:
            last_winner = (last_winner + 2) % last_num_elves
    return last_winner + 1


if __name__ == "__main__":
    the_num_elves = int(get_input(19))

    # print('Part 1:', part_1(the_num_elves))
    print('Part 2:', part_2(the_num_elves))
