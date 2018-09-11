import national_rail_fetcher

lines = national_rail_fetcher.get_board_lines()

for line in lines:
    print(line)