def find_middle_position(list):
    middle = float(len(list)) / 2
    if middle % 2 != 0:
        return int(middle - .5)
    else:
        return int(middle - 1)