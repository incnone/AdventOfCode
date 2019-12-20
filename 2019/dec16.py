def part_1(number_input):
    next_input = number_input
    for phase in range(100):
        next_input = fft_phase(next_input)
        # print('After phase {}: {}'.format(phase+1, next_input))
    print('Part 1:', ''.join([str(x) for x in next_input[:8]]))


def part_2(number_input):
    # number_input = [int(x) for x in '02935109699940807407585447034323']
    repetitions = 10**4
    total_len = len(number_input)*repetitions
    digit_idx_to_compute = int(''.join([str(x) for x in number_input[:7]])) - 1
    answer = []

    ncrs = [1]
    for n in range(100, total_len - digit_idx_to_compute + 100):
        ncrs.append(ncrs[-1]*n // (n - 99))

    for digit_idx in range(digit_idx_to_compute, digit_idx_to_compute + 8):
        next_digit = 0
        for jdx, digit_jdx in enumerate(range(digit_idx+1, total_len)):
            next_digit += (ncrs[jdx] % 10) * number_input[digit_jdx % len(number_input)]

        answer.append(next_digit % 10)

    print('Part 2:', ''.join([str(x) for x in answer]))


def fft_phase(numbers):
    base_pattern = [0, 1, 0, -1]

    output_numbers = []
    for output_stage in range(1, len(numbers)+1):
        pattern_cursor = 0
        output_value = 0
        output_repetition_counter = output_stage
        if output_stage > 1:
            output_repetition_counter -= 1
        else:
            pattern_cursor = 1

        for n in numbers:
            output_value += n*base_pattern[pattern_cursor]
            output_repetition_counter -= 1
            if output_repetition_counter == 0:
                pattern_cursor += 1
                pattern_cursor = pattern_cursor % len(base_pattern)
                output_repetition_counter = output_stage

        output_value = abs(output_value)
        output_numbers.append(output_value % 10)

    return output_numbers


if __name__ == "__main__":
    with open('input/dec16.txt', 'r') as file:
        for line in file:
            number_input_str = line

    number_array = []
    for c in number_input_str:
        number_array.append(int(c))
    part_1(number_array)
    part_2(number_array)
