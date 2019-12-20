from enum import Enum
from typing import List, Dict
from collections import defaultdict


class GateType(Enum):
    CONST = 0
    DIRECT = 1
    AND = 2
    OR = 3
    XOR = 4
    NOT = 5
    LSHIFT = 6
    RSHIFT = 7


class LogicGate(object):
    def __init__(self, gate_str):
        inputs, output = gate_str.split('->')
        inputs = inputs.split()
        self.param = None

        # Constant input or direct connection
        if len(inputs) == 1:
            try:
                self.inputs = [int(inputs[0])]
                self.gate_type = GateType.CONST
                self.output = output.strip()
            except ValueError:
                self.inputs = [inputs[0]]
                self.gate_type = GateType.DIRECT
                self.output = output.strip()

        # NOT gate
        elif len(inputs) == 2:
            if inputs[0] == 'NOT':
                self.gate_type = GateType.NOT
                self.inputs = [inputs[1].strip()]
                self.output = output.strip()
            else:
                raise RuntimeError('Unrecognized logic gate string <{}>'.format(gate_str))

        # Others
        elif len(inputs) == 3:
            if inputs[1] == 'AND':
                self.inputs = [inputs[0].strip(), inputs[2].strip()]
                self.output = output.strip()
                self.gate_type = GateType.AND
            elif inputs[1] == 'OR':
                self.inputs = [inputs[0].strip(), inputs[2].strip()]
                self.output = output.strip()
                self.gate_type = GateType.OR
            elif inputs[1] == 'XOR':
                self.inputs = [inputs[0].strip(), inputs[2].strip()]
                self.output = output.strip()
                self.gate_type = GateType.XOR
            elif inputs[1] == 'LSHIFT':
                self.inputs = [inputs[0].strip()]
                self.param = int(inputs[2])
                self.output = output.strip()
                self.gate_type = GateType.LSHIFT
            elif inputs[1] == 'RSHIFT':
                self.inputs = [inputs[0].strip()]
                self.param = int(inputs[2])
                self.output = output.strip()
                self.gate_type = GateType.RSHIFT
            else:
                raise RuntimeError('Unrecognized logic gate string <{}>'.format(gate_str))

        else:
            raise RuntimeError('Unrecognized logic gate string <{}>'.format(gate_str))

    def execute(self, wires: Dict[str, int]):
        try:
            if self.gate_type == GateType.CONST:
                wires[self.output] = self.inputs[0]
            elif self.gate_type == GateType.DIRECT:
                wires[self.output] = wires[self.inputs[0]]
            elif self.gate_type == GateType.AND:
                wires[self.output] = wires[self.inputs[0]] & wires[self.inputs[1]]
            elif self.gate_type == GateType.OR:
                wires[self.output] = wires[self.inputs[0]] | wires[self.inputs[1]]
            elif self.gate_type == GateType.XOR:
                wires[self.output] = wires[self.inputs[0]] ^ wires[self.inputs[1]]
            elif self.gate_type == GateType.NOT:
                wires[self.output] = ~wires[self.inputs[0]]
            elif self.gate_type == GateType.LSHIFT:
                wires[self.output] = wires[self.inputs[0]] << self.param
            elif self.gate_type == GateType.RSHIFT:
                wires[self.output] = wires[self.inputs[0]] >> self.param

            wires[self.output] %= 65536
        except TypeError:
            print('GATE ERROR:', self.inputs, wires)
            print(self.inputs[0], self.inputs[1], wires[self.inputs[0]], wires[self.inputs[1]])
            raise

    def __str__(self):
        return '{} --{}--> {}'.format(self.inputs, self.gate_type, self.output)


def toposort_logicgates(logic_gates: List[LogicGate]):
    logic_gates = logic_gates.copy()
    toposorted_gates = []
    gates_with_input = defaultdict(lambda: [])
    for gate in logic_gates:
        for input_val in gate.inputs:
            gates_with_input[input_val].append(gate)

    tempmarked_gates = []

    def _toposort_visit(gate):
        if gate in toposorted_gates:
            return
        if gate in tempmarked_gates:
            raise RuntimeError('Toposort called but this is not a DAG')
        tempmarked_gates.append(gate)
        for later_gate in gates_with_input[gate.output]:
            _toposort_visit(later_gate)
        tempmarked_gates.remove(gate)
        logic_gates.remove(gate)
        toposorted_gates.append(gate)

    while logic_gates:
        next_gate = logic_gates[-1]
        _toposort_visit(next_gate)

    return reversed(toposorted_gates)