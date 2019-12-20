def satisfactory_pass(num):
    num_str = str(num)
    if len(num_str) != 6:
        return False

    found_double = False
    last_digit = 0
    for digit in num_str:
        if int(digit) < last_digit:
            return False
        elif int(digit) == last_digit:
            found_double = True
        last_digit = int(digit)

    if not found_double:
        return False

    return True


def satisfactory_pass_2(num):
    num_str = str(num)
    if len(num_str) != 6:
        return False

    double_indicies = set()
    last_digit = 0
    for idx, digit in enumerate(num_str):
        if int(digit) < last_digit:
            return False
        elif int(digit) == last_digit:
            double_indicies.add(idx)

        last_digit = int(digit)

    found_double = False
    for idx in double_indicies:
        if idx+1 not in double_indicies and idx-1 not in double_indicies:
            found_double = True

    if not found_double:
        return False

    return True


if __name__ == "__main__":
    with open('input/dec4.txt', 'r') as file:
        vals = file.readline().split('-')

    minval = int(vals[0])
    maxval = int(vals[1].rstrip('\n'))

    print(minval, maxval)
    print(satisfactory_pass_2(111122))

    num_valid = 0
    for i in range(minval, maxval):
        if satisfactory_pass_2(i):
            num_valid += 1
    print(num_valid)
