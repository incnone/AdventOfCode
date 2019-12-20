def fuel_req(weight: int) -> int:
    if weight <= 8:
        return 0

    fuel = weight // 3 - 2
    return fuel + fuel_req(fuel)


if __name__ == "__main__":
    fuel = 0
    with open('input/dec1.txt', 'r') as file:
        for line in file:
            fuel += fuel_req(int(line))
    print(fuel)
