def set_dir(name, dirs):
    letter_of_movie = name[0]
    letter = letter_of_movie.upper()
    dir = ''
    if letter == 'A' or letter == 'B' or letter == 'C' or letter == 'D':
        dir = dirs + '\\A-D\\' + name
    if letter == 'E' or letter == 'F' or letter == 'G' or letter == 'H':
        dir = dirs + '\\E-H\\' + name
    if letter == 'I' or letter == 'J' or letter == 'K' or letter == 'L':
        dir = dirs + '\\I-L\\' + name
    if letter == 'M' or letter == 'N' or letter == 'O' or letter == 'P' or letter == 'Q':
        dir = dirs + '\\M-P\\' + name
    if letter == 'R' or letter == 'S' or letter == 'T' or letter == 'U':
        dir = dirs + '\\R-U\\' + name
    if letter == 'W' or letter == 'V' or letter == 'X' or letter == 'Y' or letter == 'Z':
        dir = dirs + '\\W-Z\\' + name
    return dir