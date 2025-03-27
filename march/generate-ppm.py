
'''
goal - make a ppm peit program for a specific literal
'''

import literals

MAX_VAL = 255
colors = (
        (0xffc0c0, 0xff0000, 0xc00000),
        (0xffffc0, 0xffff00, 0xc0c000),
        (0xc0ffc0, 0x00ff00, 0x00c000),
        (0xc0ffff, 0x00ffff, 0x00c0c0),
        (0xc0c0ff, 0x0000ff, 0x0000c0),
        (0xffc0ff, 0xff00ff, 0xc000c0))
black = 0x0
white = 0xffffff
instructions = (
        (None, 'push', 'pop'),
        ('add', 'subtract', 'multiply'),
        ('divide', 'mod', 'not'),
        ('greater', 'pointer', 'switch'),
        ('duplicate', 'roll', 'in(n)'),
        ('in(c)', 'out(n)', 'out(c)'))
inv_instructions = {
        'push': (0, 1), 'pop': (0, 2),
        'add': (1, 0), 'subtract': (1, 1), 'multiply': (1, 2),
        'divide': (2, 0), 'mod': (2, 1), 'not': (2, 2),
        'greater': (3, 0), 'pointer': (3, 1), 'switch': (3, 2),
        'duplicate': (4, 0), 'roll': (4, 1), 'in(n)': (4, 2),
        'in(c)': (5, 0), 'out(n)': (5, 1), 'out(c)': (5, 2)}


def str_to_list(instrs: str) -> [str]:
    return [literals.instructions[i] for i in instrs]


def ops_to_pixels(instrs: [str]) -> [[int]]:
    ''' convert list of instructions to pixel array '''
    pass


def pixel_to_rgb(pixel: int) -> [int, int, int]:
    r = pixel >> 0x10
    g = (pixel >> 0x8) & 0xff
    b = pixel & 0xff
    return r, g, b


def padding(r: int, g: int, b: int) -> str:
    ret = []
    for i in [r, g, b]:
        if i >= 100:
            ret.append(str(i))
        elif i >= 10:
            ret.append(' ' + str(i))
        else:
            ret.append('  ' + str(i))
    return ' '.join(ret)


def pixels_to_ppm(pixels: [[int]]) -> str:
    ''' pixel array to plain ppm string '''
    lines = ['P3']
    lines.append('# tool assisted image')
    lines.append(str(len(pixels[0])) + ' ' + str(len(pixels)))
    lines.append(str(MAX_VAL))
    for line in pixels:
        ln = []
        for pixel in line:
            r, g, b = pixel_to_rgb(pixel)
            ln.append(padding(r, g, b))
        lines.append('  '.join(ln))
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    cases = ('pda', 'ms', '')
    truth = (['push', 'dup', 'add'],
             ['mult', 'sub'],
             [])
    for i in range(len(truth)):
        assert str_to_list(cases[i]) == truth[i]

    cases = (['push', 'dup', 'add'],
             ['pop', 'pop'],
             ['subtract', 'mod', 'not', 'greater', 'pointer', 'switch',
              'roll', 'in(n)', 'in(c)', 'out(n)', 'out(c)'])
    truth = ([0xffc0c0, 0xff0000, 0xff, 0xff00ff],
             [0xffc0c0, 0xc00000, 0xff0000],
             [0xffc0c0, 0xffff00, 0x00c0c0, 0xff00ff, 0xff00, 0xc000c0,
              0xff00, 0xc00000, 0xff, 0xffff, 0xc000, 0xffff00])
    for i in range(len(truth)):
        assert ops_to_pixels(cases[i]) == truth[i]

    cases = colors[0]
    truth = ((0xff, 0xc0, 0xc0), (0xff, 0, 0), (0xc0, 0, 0))
    for i in range(len(truth)):
        assert pixel_to_rgb(cases[i]) == truth[i]

    cases = ((0xff, 0xff, 0xff), (0xff, 0xc0, 0), (0, 0, 0))
    truth = ('255 255 255', '255 192   0', '  0   0   0')
    for i in range(len(truth)):
        r, g, b = cases[i]
        assert padding(r, g, b) == truth[i]

    cases = (
            ((0xffffff, 0xffc000),
             (0x031464, 0x00c0ff)),
            ([0xffc000],
             [0x00c0ff])
            )
    truth = (
            '''P3
# tool assisted image
2 2
255
255 255 255  255 192   0
  3  20 100    0 192 255
''',
            '''P3
# tool assisted image
1 2
255
255 192   0
  0 192 255
'''
            )
    for i in range(len(truth)):
        assert pixels_to_ppm(cases[i]) == truth[i], pixels_to_ppm(cases[i])
