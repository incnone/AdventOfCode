from getinput import get_input


def parse_into_triples(inputstr):
    triples = []
    for line in inputstr.splitlines(keepends=False):
        triples.append(tuple(int(c) for c in line.split('x')))
    return triples


def get_needed_wrapping_paper(x, y, z):
    return 2*x*y + 2*x*z + 2*y*z + min(x*y, x*z, y*z)


def get_needed_ribbon(x, y, z):
    return 2*min(x+y, x+z, y+z) + x*y*z


def part_1(inputstr):
    return sum(get_needed_wrapping_paper(*present) for present in parse_into_triples(inputstr))


def part_2(inputstr):
    return sum(get_needed_ribbon(*present) for present in parse_into_triples(inputstr))


if __name__ == "__main__":
    the_inputstr = get_input(2)

    print('Part 1:', part_1(the_inputstr))
    print('Part 2:', part_2(the_inputstr))
