import generate_ppm
import literals

'''
goal - generate the actual painting here

rough canvas size - start with 30 - by 15 |
    giving a 9  - by 15 | rhs
             21 - by 15 | lhs
'''


def gen_bw_grid(width: int, height: int) -> [[int]]:
    rows = []
    for i in range(height):
        if i % 2 == 0:
            row = [0xffffff] * width
        else:
            row = ([0xffffff, 0] * (width // 2)) + [0xffffff]
        rows.append(row)
    return rows


def poc():
    ''' proof of concept for the vision '''
    from random import randint
    grid = []
    for i in gen_bw_grid(21, 15):
        for _ in range(10):
            i += [randint(0, 0xffffff)]
        grid.append(i)
    print(generate_ppm.pixels_to_ppm(grid))


def functional_section():
    ''' generate literal, operate, secret message, destroy, repeat '''
    p, q = 1048583, 1048589
    n = p * q
    instrs = generate_ppm.str_to_list(literals.best(n))
    pixels = generate_ppm.ops_to_pixels(instrs)
    # pad = [0xffffff] * len(pixels)
    pix2 = []
    buf = []
    for i in range(len(pixels)):
        buf.append(pixels[i])
        if i % 10 == 9:
            pix2.append(buf)
            buf = []
    pix2.append(buf + [0xffffff]*4)
    print(generate_ppm.pixels_to_ppm(pix2))
    # TODO: finish
