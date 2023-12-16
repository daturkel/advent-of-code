not too hard today. i chose an implementation for part 1 that happened to be extremely convenient for part 2 since it's time complexity isn't dependant on the size of the expansion.

i only go through the original input once, during which i:
collect the galaxy locations
make note of which rows and columns are not empty, removing those indexes from an empty_columns and empty_rows list
Then I make a mapping of original coordinates to expanded coordinate:
    for empty_col in empty_columns:
        # all columns/rows *after* the empty one are pushed outward
        for col in range(empty_col, width):
            col_map_a[col] += 1
            col_map_b[col] += 999999
Then I calculate manhattan distances using the mapped coordinates:
        dx_a = abs(col_map_a[xb] - col_map_a[xa])
        dy_a = abs(row_map_a[yb] - row_map_a[ya])
        total_distance_a += dx_a + dy_a
We get unique combinations of galaxies for free from python’s itertools.combinations