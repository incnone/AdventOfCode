from intcode import IntcodeProgram, IOHandlerL2C


def part_1(program_code):
    program = IntcodeProgram(program_code)
    program.execute()
    ret = []
    retline = []
    for x in program.outputter.output_list:
        if chr(x) == '\n' and retline:
            ret.append(retline.copy())
            retline = []
        else:
            retline.append(chr(x))

    with open('input/dec_17_out.txt', 'w') as file:
        file.write('\n'.join([''.join([c for c in l]) for l in ret]))

    intersections = []
    for y in range(len(ret)):
        for x in range(len(ret[y])):
            if ret[y][x] == '#':
                intersection = True
                for a, b in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    try:
                        if ret[y + b][x + a] != '#':
                            intersection = False
                    except IndexError:
                        intersection = False
                if intersection:
                    intersections.append((x, y))

    t = 0
    for x, y in intersections:
        t += x*y
    print(t)


def convert_output_pic(ascii_list):
    return ''.join([chr(c) for c in ascii_list])


def part_2(program_code):
    program = IntcodeProgram(program_code, io_handler=IOHandlerL2C(use_ascii=True))
    movement_A = [ord(x) for x in 'R,8,L,12,R,8\n']
    movement_B = [ord(x) for x in 'L,12,L,12,L,10,R,10\n']
    movement_C = [ord(x) for x in 'L,10,L,10,R,8\n']
    movement_P = [ord(x) for x in 'A,A,C,B,C,B,C,A,B,A\n']

    program.code[0] = 2
    program.io_handler.input_list = movement_P + movement_A + movement_B + movement_C + [ord('n'), ord('\n')]
    program.execute()
    # print(convert_output_pic(program.outputter.output_list))
    # print(program.outputter.output_list[-1])


if __name__ == "__main__":
    with open('input/dec17.txt', 'r') as file:
        for line in file:
            program_code_input = line

    # part_1(program_code_input)
    part_2(program_code_input)
