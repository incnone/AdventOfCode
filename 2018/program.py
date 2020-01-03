import string


class Program(object):
    @staticmethod
    def all_opcodes():
        return [
            Program.addr,
            Program.addi,
            Program.mulr,
            Program.muli,
            Program.banr,
            Program.bani,
            Program.borr,
            Program.bori,
            Program.setr,
            Program.seti,
            Program.gtir,
            Program.gtri,
            Program.gtrr,
            Program.eqir,
            Program.eqri,
            Program.eqrr,
        ]

    @staticmethod
    def get_opcode(s):
        opcodes = {
            'addr': Program.addr,
            'addi': Program.addi,
            'mulr': Program.mulr,
            'muli': Program.muli,
            'banr': Program.banr,
            'bani': Program.bani,
            'borr': Program.borr,
            'bori': Program.bori,
            'setr': Program.setr,
            'seti': Program.seti,
            'gtir': Program.gtir,
            'gtri': Program.gtri,
            'gtrr': Program.gtrr,
            'eqir': Program.eqir,
            'eqri': Program.eqri,
            'eqrr': Program.eqrr,
        }
        return opcodes[s]

    def __init__(self):
        self.reg = [0, 0, 0, 0, 0, 0]
        self.instr_ptr_idx = None
        self.instrs = []

    @property
    def instr_ptr(self):
        return self.reg[self.instr_ptr_idx]

    def execute(self):
        while 0 <= self.instr_ptr < len(self.instrs):
            self.execute_next()

    def execute_next(self):
        opcode, a, b, c = self.instrs[self.instr_ptr]
        opcode(self, a, b, c)
        self.reg[self.instr_ptr_idx] += 1

    def init_from_str(self, s):
        self.reg = [0, 0, 0, 0, 0, 0]
        self.instrs = []
        lines = s.splitlines(keepends=False)
        self.instr_ptr_idx = int(lines[0].split()[-1])
        for line in lines[1:]:
            words = line.split()
            opcode = Program.get_opcode(words[0])
            a, b, c = (int(x) for x in words[1:])
            self.instrs.append((opcode, a, b, c))

    def addr(self, a, b, c):
        self.reg[c] = self.reg[a] + self.reg[b]

    def addi(self, a, b, c):
        self.reg[c] = self.reg[a] + b

    def mulr(self, a, b, c):
        self.reg[c] = self.reg[a] * self.reg[b]

    def muli(self, a, b, c):
        self.reg[c] = self.reg[a] * b

    def banr(self, a, b, c):
        self.reg[c] = self.reg[a] & self.reg[b]

    def bani(self, a, b, c):
        self.reg[c] = self.reg[a] & b

    def borr(self, a, b, c):
        self.reg[c] = self.reg[a] | self.reg[b]

    def bori(self, a, b, c):
        self.reg[c] = self.reg[a] | b

    def setr(self, a, b, c):
        self.reg[c] = self.reg[a]

    def seti(self, a, b, c):
        self.reg[c] = a

    def gtir(self, a, b, c):
        self.reg[c] = 1 if a > self.reg[b] else 0

    def gtri(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] > b else 0

    def gtrr(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] > self.reg[b] else 0

    def eqir(self, a, b, c):
        self.reg[c] = 1 if a == self.reg[b] else 0

    def eqri(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] == b else 0

    def eqrr(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] == self.reg[b] else 0


class Decompile(object):
    @staticmethod
    def get_opcode(s):
        opcodes = {
            'addr': Decompile.addr,
            'addi': Decompile.addi,
            'mulr': Decompile.mulr,
            'muli': Decompile.muli,
            'banr': Decompile.banr,
            'bani': Decompile.bani,
            'borr': Decompile.borr,
            'bori': Decompile.bori,
            'setr': Decompile.setr,
            'seti': Decompile.seti,
            'gtir': Decompile.gtir,
            'gtri': Decompile.gtri,
            'gtrr': Decompile.gtrr,
            'eqir': Decompile.eqir,
            'eqri': Decompile.eqri,
            'eqrr': Decompile.eqrr,
        }
        return opcodes[s]
    
    def __init__(self, ip_register):
        self.ipr = ip_register
        self.idx = 0

    def reg(self, n):
        if n == self.ipr:
            return self.idx
        else:
            return string.ascii_lowercase[n]

    def decompile(self, idx, s):
        self.idx = idx
        words = s.split()
        opcode = Decompile.get_opcode(words[0])
        a, b, c = (int(x) for x in words[1:])
        return '{:>3}: {}'.format(idx, opcode(self, a, b, c))
    
    def addr(self, a, b, c):
        if c == self.ipr:
            if a == self.ipr:
                return 'jump {}+1'.format(self.reg(b))
            elif b == self.ipr:
                return 'jump {}+1'.format(self.reg(a))
            else:
                return 'goto {}+{}+1'.format(self.reg(a), self.reg(b))
        else:
            if c == a:
                return '{} += {}'.format(self.reg(c), self.reg(b))
            elif c == b:
                return '{} += {}'.format(self.reg(c), self.reg(a))
            else:
                return '{} = {}+{}'.format(self.reg(c), self.reg(a), self.reg(b))

    def addi(self, a, b, c):
        if c == self.ipr:
            if a == self.ipr:
                return 'jump {}'.format(b+1)
            else:
                return 'goto {}+{}'.format(self.reg(a), b+1)
        else:
            if c == a:
                return '{} += {}'.format(self.reg(c), b)
            elif c == b:
                return '{} += {}'.format(self.reg(c), self.reg(a))
            else:
                return '{} = {}+{}'.format(self.reg(c), self.reg(a), b)

    def mulr(self, a, b, c):
        if c == self.ipr:
            if a == self.ipr:
                return 'wtf {}'.format(self.reg(b))
            elif b == self.ipr:
                return 'wtf {}'.format(self.reg(a))
            else:
                return 'goto {}*{}+1'.format(self.reg(a), self.reg(b))
        else:
            if c == a:
                return '{} *= {}'.format(self.reg(c), self.reg(b))
            elif c == b:
                return '{} *= {}'.format(self.reg(c), self.reg(a))
            else:
                return '{} = {}*{}'.format(self.reg(c), self.reg(a), self.reg(b))

    def muli(self, a, b, c):
        if c == self.ipr:
            if a == self.ipr:
                return 'wtf {}'.format(b)
            else:
                return 'goto {}*{}+1'.format(self.reg(a), b)
        else:
            if c == a:
                return '{} *= {}'.format(self.reg(c), b)
            elif c == b:
                return '{} *= {}'.format(self.reg(c), self.reg(a))
            else:
                return '{} = {}*{}'.format(self.reg(c), self.reg(a), b)

    def banr(self, a, b, c):
        if c == self.ipr:
            return 'goto {}&{}+1'.format(self.reg(a), self.reg(b))
        else:
            return '{} = {}&{}'.format(self.reg(c), self.reg(a), self.reg(b))

    def bani(self, a, b, c):
        if c == self.ipr:
            return 'goto {}&{}+1'.format(self.reg(a), bin(b))
        else:
            return '{} = {}&{}'.format(self.reg(c), self.reg(a), bin(b))
    
    def borr(self, a, b, c):
        if c == self.ipr:
            return 'goto {}|{}+1'.format(self.reg(a), self.reg(b))
        else:
            return '{} = {}|{}'.format(self.reg(c), self.reg(a), self.reg(b))

    def bori(self, a, b, c):
        if c == self.ipr:
            return 'goto {}|{}+1'.format(self.reg(a), bin(b))
        else:
            return '{} = {}|{}'.format(self.reg(c), self.reg(a), bin(b))
    
    def setr(self, a, b, c):
        if c == a:
            return 'nop'
        elif c == self.ipr:
            return 'goto {}+1'.format(self.reg(a))
        else:
            return '{} = {}'.format(self.reg(c), self.reg(a))
    
    def seti(self, a, b, c):
        if c == self.ipr:
            return 'goto {}'.format(a+1)
        else:
            return '{} = {}'.format(self.reg(c), a)
    
    def gtir(self, a, b, c):
        if c == self.ipr:
            return 'gtir(ip) NOT IMPLEMENTED IN DECOMPILER'
        else:
            return '{} = ({} < {})'.format(self.reg(c), self.reg(b), a)
    
    def gtri(self, a, b, c):
        if c == self.ipr:
            return 'gtri(ip) NOT IMPLEMENTED IN DECOMPILER'
        else:
            return '{} = ({} < {})'.format(self.reg(c), b, self.reg(a))
    
    def gtrr(self, a, b, c):
        if c == self.ipr:
            return 'gtrr(ip) NOT IMPLEMENTED IN DECOMPILER'
        else:
            return '{} = ({} < {})'.format(self.reg(c), self.reg(b), self.reg(a))
    
    def eqir(self, a, b, c):
        if c == self.ipr:
            return 'eqir(ip) NOT IMPLEMENTED IN DECOMPILER'
        else:
            return '{} = ({} == {})'.format(self.reg(c), self.reg(b), a)
    
    def eqri(self, a, b, c):
        if c == self.ipr:
            return 'eqri(ip) NOT IMPLEMENTED IN DECOMPILER'
        else:
            return '{} = ({} == {})'.format(self.reg(c), b, self.reg(a))
    
    def eqrr(self, a, b, c):
        if c == self.ipr:
            return 'gtrr(ip) NOT IMPLEMENTED IN DECOMPILER'
        else:
            return '{} = ({} == {})'.format(self.reg(c), self.reg(b), self.reg(a))
