import generate_ppm
import literals

DEBUG = False


def dprint(m):
    if DEBUG:
        print(m)


'''
goal - generate the actual painting here

rough canvas size - start with 30 - by 15 |
    giving a 9  - by 15 | rhs
             21 - by 15 | lhs
'''
WIDTH = 42
HEIGHT = WIDTH // 2


def gen_bw_grid(width: int, height: int) -> [[int]]:
    rows = []
    for i in range(height):
        if i % 2 == 0:
            row = [0xffffff] * width
        else:
            row = ([0xffffff, 0] * (width // 2)) + [0xffffff]
        rows.append(row)
    return rows


def wrap(ops: [str], width: int, direction='r') -> [[int]]:
    ''' add rhs and lhs wraps to fit ops within width '''
    pixels = []
    i = 2
    row = []
    last = None
    for op in ops:
        row.append(op)
        if direction == 'r':
            if i == (width - 3):
                row += ['push', 'push', 'pointer']
                dprint(row)
                i = 1
                direction = 'l'
                pixel_row = generate_ppm.ops_to_pixels(
                        row, last if last else 0xffc0c0)
                if last:
                    pixel_row = pixel_row[1:]
                last = pixel_row[-1]
                pixels.append(pixel_row)
                row = ['pointer']
        else:
            if i == (width - 7):
                row += ['push', 'push', 'push', 'add',
                        'add', 'duplicate', 'pointer']
                dprint(row)
                i = 1
                direction = 'r'
                pixel_row = generate_ppm.ops_to_pixels(row, last)[1:][::-1]
                last = pixel_row[0]
                pixels.append(pixel_row)
                row = ['pointer']
        i += 1
    dprint(row)
    pixel_row = generate_ppm.ops_to_pixels(row, last)[1:]
    pad = width - len(pixel_row)
    if direction == 'r':
        pixel_row += [generate_ppm.white] * pad
    else:
        pixel_row = pad * [generate_ppm.white] + pixel_row
    pixels.append(pixel_row)
    return pixels


def poc():
    ''' proof of concept for the vision '''
    from random import randint
    grid = []
    for i in gen_bw_grid(21, 15):
        for _ in range(10):
            i += [randint(0, 0xffffff)]
        grid.append(i)
    print(generate_ppm.pixels_to_ppm(grid))


def _init():
    p, q = 1048583, 1048589
    n = p * q
    c = generate_ppm.str_to_list(literals.best(3))
    instrs = generate_ppm.str_to_list(literals.best(n))
    pixels = wrap(c + instrs, WIDTH // 3)
    return pixels


def functional_section():
    ''' generate literal, operate, secret message, destroy, repeat '''
    grid = gen_bw_grid(int(WIDTH * .66), HEIGHT)
    init = _init()
    init += [[]] * (len(grid) - len(init))
    final = []
    target = len(init[0]) + len(grid[0])
    for i in range(len(grid)):
        final.append(grid[i] + init[i])
        final[-1] += [generate_ppm.white] * (target - len(final[-1]))
    print(generate_ppm.pixels_to_ppm(final))


functional_section()
