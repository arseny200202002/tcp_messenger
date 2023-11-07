state_tree = {
    1: {'LOGIN': 2, 'REGISTER': 3},
    2: {'DATA': 4, 'BACK': 1},
    3: {'DATA': 4, 'BACK': 1},
    4: {'CREATE': 5, 'DATA': 6, 'BACK': 1},
    5: {'DATA': 6, 'BACK': 4},
    6: {'DATA': 6, 'BACK': 5},
}

commands = list(state_tree[2].keys())

print('BACK' not in commands)