
'''
goal - make a ppm peit program for a specific literal
'''

import literals

colors = [
        [0xffc0c0, 0xff0000, 0xc00000],
        [0xffffc0, 0xffff00, 0xc0c000],
        [0xc0ffc0, 0x00ff00, 0x00c000],
        [0xc0ffff, 0x00ffff, 0x00c0c0],
        [0xc0c0ff, 0x0000ff, 0x0000c0],
        [0xffc0ff, 0xff00ff, 0xc000c0]]
instructions = [
        [None, 'push', 'pop'],
        ['add', 'subtract', 'multiply'],
        ['divide', 'mod', 'not'],
        ['greater', 'pointer', 'switch'],
        ['duplicate', 'roll', 'in(n)'],
        ['in(c)', 'out(n)', 'out(c)']]
inv_instructions = {
        'push' : (0,1), 'pop' : (0,2),
        'add' : (1,0), 'subtract' : (1,1), 'multiply' : (1,2),
        'divide' : (2,0), 'mod' : (2,1), 'not' : (2,2),
        'greater' : (3,0), 'pointer' : (3,1), 'switch' : (3,2),
        'duplicate' : (4,0), 'roll' : (4,1), 'in(n)' : (4,2),
        'in(c)' : (5,0), 'out(n)' : (5,1), 'out(c)' : (5,2)}

def str_to_list(instrs:str) -> [str]:
    for i in instrs:
        yield literals.instructions[i]


