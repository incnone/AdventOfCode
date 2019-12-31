from getinput import get_input


def parse_input(s):
    scanners = dict()
    for line in s.splitlines(keepends=False):
        vals = line.split(':')
        scanners[int(vals[0])] = int(vals[1])
    return scanners


def is_caught(scanners, packet_delay):
    for dist, depth in scanners.items():
        cycle_length = 2*depth - 2
        if (dist + packet_delay) % cycle_length == 0:
            return True
    return False


def part_1(input_str):
    scanners = parse_input(input_str)
    severity = 0
    for dist, depth in scanners.items():
        cycle_length = 2*depth - 2
        if dist % cycle_length == 0:
            severity += dist*depth
    return severity


def part_2(input_str):
    """This is fast enough because is_caught is fast, but there should be a number theory way to do this orders of
    magnitude faster"""
    scanners = parse_input(input_str)
    delay = 0
    while True:
        if not is_caught(scanners, delay):
            break
        delay += 1
    return delay


def main():
    input_str = get_input(13)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
