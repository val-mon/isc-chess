def print_squares(squares):
    count = 0
    line = ""
    for square in squares:
        count += 1
        line += f"{square} "
        if count == 8:
            print()
            print(line)
            count = 0
            line = ""
