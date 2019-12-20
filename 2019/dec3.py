class WireSegment(object):
    def __init__(self, start, dir_spec, prelength):
        self.upper_left = tuple(start)
        self.horizontal = dir_spec[0] in {'L', 'R'}
        self.length = int(dir_spec[1:])
        self.prelength = prelength
        self.inverted = False
        if dir_spec[0] == 'U':
            self.upper_left = (self.upper_left[0], self.upper_left[1] - self.length)
            self.inverted = True
        elif dir_spec[0] == 'L':
            self.upper_left = (self.upper_left[0] - self.length, self.upper_left[1])
            self.inverted = True

    def __repr__(self):
        return "Wire Segment starting at ({x}, {y}), {horiz}, length {len}".format(
            x=self.upper_left[0],
            y=self.upper_left[1],
            horiz='horizontal' if self.horizontal else 'vertical',
            len=self.length
        )

    def crosses(self, other):
        if self.horizontal == other.horizontal:
            return None

        if self.horizontal:
            horiz = self
            vert = other
        else:
            horiz = other
            vert = self

        if 0 <= vert.upper_left[0] - horiz.upper_left[0] <= horiz.length \
                and 0 <= horiz.upper_left[1] - vert.upper_left[1] <= vert.length:
            return vert.upper_left[0], horiz.upper_left[1]

    def crosses_len(self, other):
        if self.horizontal == other.horizontal:
            return None

        if self.horizontal:
            horiz = self
            vert = other
        else:
            horiz = other
            vert = self

        if 0 <= vert.upper_left[0] - horiz.upper_left[0] <= horiz.length \
                and 0 <= horiz.upper_left[1] - vert.upper_left[1] <= vert.length:
            horiz_dist = vert.upper_left[0] - horiz.upper_left[0]
            vert_dist = horiz.upper_left[1] - vert.upper_left[1]
            if horiz.inverted:
                horiz_dist = horiz.length - horiz_dist
            if vert.inverted:
                vert_dist = vert.length - vert_dist
            return horiz.prelength + horiz_dist + vert.prelength + vert_dist


class Wire(object):
    def __init__(self, dir_spec_str):
        self.wires = []
        dir_specs = dir_spec_str.split(',')
        position = [0, 0]
        length_so_far = 0
        for dir_spec in dir_specs:
            self.wires.append(WireSegment(start=position, dir_spec=dir_spec.rstrip('\n'), prelength=length_so_far))
            direction = dir_spec[0]
            length = int(dir_spec[1:].rstrip('\n'))
            if direction == 'U':
                position[1] -= length
            elif direction == 'D':
                position[1] += length
            elif direction == 'L':
                position[0] -= length
            elif direction == 'R':
                position[0] += length
            length_so_far += length


if __name__ == "__main__":
    with open('input/dec3.txt', 'r') as file:
        wire1 = Wire(file.readline())
        wire2 = Wire(file.readline())

    # wire1 = Wire('R8,U5,L5,D3')
    # wire2 = Wire('U7,R6,D4,L4')

    # wire1 = Wire('R75,D30,R83,U83,L12,D49,R71,U7,L72')
    # wire2 = Wire('U62,R66,U55,R34,D71,R55,D58,R83')

    crosslens = set()
    for ws1 in wire1.wires:
        for ws2 in wire2.wires:
            crossing = ws1.crosses_len(ws2)
            if crossing is not None and crossing != 0:
                crosslens.add(crossing)

    print(min(crosslens))
