from collections import defaultdict


def part_1(image_data, width, height):
    digit_counts = defaultdict(lambda: [0, 0, 0])
    num_layers = len(image_data)//(width*height)
    cursor = 0
    for layer in range(num_layers):
        while cursor < width*height*layer:
            if image_data[cursor] == '0':
                digit_counts[layer][0] += 1
            elif image_data[cursor] == '1':
                digit_counts[layer][1] += 1
            elif image_data[cursor] == '2':
                digit_counts[layer][2] += 1
            cursor += 1

    print(sorted(digit_counts.items(), key=lambda p: p[1][0]))


def stack_layer(layer_top, layer_bottom):
    stacked_layer = ''
    for t, b in zip(layer_top, layer_bottom):
        stacked_layer += t if t != '2' else b
    return stacked_layer


def part_2(image_data, width, height):
    layer_size = width*height
    num_layers = len(image_data)//layer_size
    final_image = '2'*layer_size
    for layer in range(num_layers):
        final_image = stack_layer(final_image, image_data[layer*layer_size:(layer+1)*layer_size])

    for line in range(height):
        print(final_image[line*width:(line+1)*width])


if __name__ == "__main__":
    with open('input/dec8.txt') as file:
        for line in file:
            image_data = line.rstrip('\n')

    part_1(image_data, width=25, height=6)
    part_2(image_data, width=25, height=6)
