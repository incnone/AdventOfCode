import textwrap
import re


class TicketData(object):
    def __init__(self, fields, yours, nearby):
        self.fields = fields
        self.yours = yours
        self.nearby = nearby


def get_test_input() -> str:
    return textwrap.dedent("""\
    class: 0-1 or 4-19
    row: 0-5 or 8-19
    seat: 0-13 or 16-19
    
    your ticket:
    11,12,13
    
    nearby tickets:
    3,9,18
    15,1,5
    5,14,9""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    ticket_fields = dict()
    your_ticket = []
    nearby_tickets = []

    sections = s.split('\n\n')

    fields_re = re.compile(r'(?P<name>[^:]+): (?P<a1>\d+)-(?P<a2>\d+) or (?P<b1>\d+)-(?P<b2>\d+)')
    for line in sections[0].splitlines():
        match = fields_re.match(line)
        ticket_fields[match['name']] = [(int(match['a1']), int(match['a2'])), (int(match['b1']), int(match['b2']))]

    for val in sections[1].splitlines()[1].split(','):
        your_ticket.append(int(val))

    for line in sections[2].splitlines()[1:]:
        this_ticket = []
        for val in line.split(','):
            this_ticket.append(int(val))
        nearby_tickets.append(this_ticket)

    return TicketData(ticket_fields, your_ticket, nearby_tickets)


def part_1(data):
    sum_of_invalids = 0
    for ticket in data.nearby:
        for val in ticket:
            if not any(range_1[0] <= val <= range_1[1] or range_2[0] <= val <= range_2[1]
                       for range_1, range_2 in data.fields.values()):
                sum_of_invalids += val
    print('Part 1:', sum_of_invalids)


def part_2(data):
    valid_tickets = []
    for ticket in data.nearby:
        if all(
                any(range_1[0] <= val <= range_1[1] or range_2[0] <= val <= range_2[1]
                    for range_1, range_2 in data.fields.values())
                for val in ticket
        ):
            valid_tickets.append(ticket)

    fields_possible = []
    for _ in data.fields:
        fields_possible.append([field for field in data.fields.keys()])

    for idx, possible_list in enumerate(fields_possible):
        fields_possible[idx] = [
            f for f in possible_list if
            all(
                data.fields[f][0][0] <= ticket[idx] <= data.fields[f][0][1]
                or data.fields[f][1][0] <= ticket[idx] <= data.fields[f][1][1]
                for ticket in valid_tickets
            )
        ]

    seen_fields = set()
    while any(len(v) > 1 for v in fields_possible):
        for idx, possible_list in enumerate(fields_possible):
            if len(possible_list) == 1 and possible_list[0] not in seen_fields:
                seen_fields.add(possible_list[0])
                new_fields_possible = []
                for jdx, pl in enumerate(fields_possible):
                    if idx == jdx:
                        new_fields_possible.append(pl)
                    else:
                        new_fields_possible.append([x for x in pl if x != possible_list[0]])
                fields_possible = new_fields_possible
                break

    ticket_prod = 1
    for idx, fieldname in enumerate(fields_possible):
        assert len(fieldname) == 1
        if fieldname[0].startswith('departure'):
            ticket_prod *= data.yours[idx]
    print('Part 2:', ticket_prod)


def main():
    data = read_input(day_number=16, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
