from getinput import get_input
import textwrap


class IPv7(object):
    def __init__(self, s):
        self.std_sequences = []
        self.hypernet_sequences = []

        current_str = ''
        for c in s:
            if c == '[':
                if current_str:
                    self.std_sequences.append(current_str)
                    current_str = ''
            elif c == ']':
                if current_str:
                    self.hypernet_sequences.append(current_str)
                    current_str = ''
            else:
                current_str += c
        self.std_sequences.append(current_str)

    @staticmethod
    def _contains_abba(s):
        for s1, s2, s3, s4 in zip(s, s[1:], s[2:], s[3:]):
            if s1 == s4 and s2 == s3 and s1 != s2:
                return True
        return False

    @staticmethod
    def _get_abas(s):
        abas = []
        for s1, s2, s3 in zip(s, s[1:], s[2:]):
            if s1 == s3 and s2 != s1:
                abas.append((s1, s2))
        return abas

    @staticmethod
    def _contains_bab(s, aba):
        return ''.join([aba[1], aba[0], aba[1]]) in s

    def supports_tls(self):
        return \
            not any(self._contains_abba(s) for s in self.hypernet_sequences) \
            and any(self._contains_abba(s) for s in self.std_sequences)

    def supports_ssl(self):
        abas = []
        for s in self.std_sequences:
            abas += self._get_abas(s)
        for s in self.hypernet_sequences:
            for aba in abas:
                if self._contains_bab(s, aba):
                    return True
        return False

    def __str__(self):
        return str(self.std_sequences) + str(self.hypernet_sequences)


def part_1(big_str):
    ips = []
    for ipstr in big_str.splitlines(keepends=False):
        ips.append(IPv7(ipstr))

    return sum(1 for ip in ips if ip.supports_tls())


def part_2(big_str):
    ips = []
    for ipstr in big_str.splitlines(keepends=False):
        ips.append(IPv7(ipstr))

    return sum(1 for ip in ips if ip.supports_ssl())


def test_str():
    return textwrap.dedent("""\
    aba[bab]xyz
    xyx[xyx]xyx
    aaa[kek]eke
    zazbz[bzb]cdb""")


if __name__ == "__main__":
    the_big_str = get_input(7)

    # print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
