class IntcodeProgram(object):
    def __init__(self, code: str):
        self.nums = [int(s) for s in code.split(',')]
        self.cursor = 0
        self.halt = False

    def read(self):
        instr = self.nums[self.cursor]
        if instr == 99:
            self.halt = True
            return

        addr1 = self.nums[self.cursor + 1]
        addr2 = self.nums[self.cursor + 2]
        addr3 = self.nums[self.cursor + 3]
        if instr == 1:    # Addition
            self.nums[addr3] = self.nums[addr1] + self.nums[addr2]
        elif instr == 2:    # Multiplication
            self.nums[addr3] = self.nums[addr1] * self.nums[addr2]

        self.cursor += 4

    def execute(self):
        while not self.halt:
            self.read()


if __name__ == "__main__":
    for i in range(99):
        for j in range(99):
            with open('input/dec2.txt', 'r') as file:
                prog = IntcodeProgram(file.readline())

            prog.nums[1] = i
            prog.nums[2] = j
            prog.execute()
            if prog.nums[0] == 19690720:
                print(100*i + j)
