from intcode import IntcodeProgram


class NetworkIOHandler(object):
    def __init__(self, address, io_controller):
        self.address = address
        self.io_controller = io_controller
        self.input_buffer = [self.address]
        self.output_buffer = []
        self._idle_checker = 10

    @property
    def idle(self):
        return self._idle_checker <= 0

    def get_input(self):
        if self.input_buffer:
            return self.input_buffer.pop(0)
        else:
            self._idle_checker = max(self._idle_checker - 1, 0)
            return -1

    def read_output(self, value):
        self.output_buffer.append(value)
        if len(self.output_buffer) == 3:
            self.io_controller.send_packet(address=self.output_buffer[0], packet=self.output_buffer[1:])
            self.output_buffer = []

    def read_packet(self, packet):
        self.input_buffer += packet
        self._idle_checker = 10


class NetworkIOController(object):
    def __init__(self):
        self.programs = dict()
        self.nat_packet = None
        self.last_sent_nat_yval = None

    def attach(self, io_handler, program_code):
        program = IntcodeProgram(program_code, io_handler)
        self.programs[io_handler.address] = program

    def send_packet(self, address, packet):
        if address == 255:
            self.nat_packet = packet
        else:
            self.programs[address].io_handler.read_packet(packet)

    def execute_step(self):
        any_executed = False
        any_nonidle = False
        for program in self.programs.values():
            if not program.halt:
                program.execute_next()
                any_executed = True
            if not program.io_handler.idle:
                any_nonidle = True

        if not any_nonidle:
            self.send_packet(address=0, packet=self.nat_packet)
            if self.nat_packet[1] == self.last_sent_nat_yval:
                print('WINNER:', self.nat_packet[1])
                exit(0)
            self.last_sent_nat_yval = self.nat_packet[1]
            print(self.last_sent_nat_yval)

        return any_executed

    def execute(self):
        while self.execute_step():
            pass


def main():
    with open('input/dec23.txt') as file:
        program_code = file.read()
    part_1(program_code)


def part_1(program_code):
    io_controller = NetworkIOController()
    for address in range(50):
        io_handler = NetworkIOHandler(address=address, io_controller=io_controller)
        io_controller.attach(io_handler, program_code)
    io_controller.execute()


def part_2(program_code):
    pass


if __name__ == "__main__":
    main()
