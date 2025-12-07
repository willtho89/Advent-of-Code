from time import perf_counter
from lib.matrix import Matrix


def part1(matrix: Matrix) -> int:
    start_row, start_col = matrix.find_start()

    splits: int = 0
    active_cols: set[int] = {start_col}

    for row in range(start_row + 1, m):
        if not active_cols:
            break
        next_active: set[int] = set()

        for col in active_cols:
            if col < 0 or col >= n:
                # exited
                continue

            cell = matrix[[row, col]]

            if cell == '^':
                # split
                splits += 1
                if col - 1 >= 0:
                    next_active.add(col - 1)
                if col + 1 < n:
                    next_active.add(col + 1)
            else:
                # downwards
                next_active.add(col)

        active_cols = next_active

    return splits


def part2(matrix: Matrix) -> int:
    start_row, start_col = matrix.find_start()
    ways: dict[int, int] = {start_col: 1}
    timelines: int = 0
    for row in range(start_row + 1, m):
        next_ways: dict[int, int] = {}
        for col, count in ways.items():
            cell = matrix[[row, col]]
            if cell == '^':
                # Split
                for new_col in (col - 1, col + 1):
                    new_row = row + 1
                    if new_row >= m or new_col < 0 or new_col >= n:
                        # exit
                        timelines += count
                    else:
                        next_ways[new_col] = next_ways.get(new_col, 0) + count
            else:
                # down
                new_row = row + 1
                new_col = col
                if new_row >= m or new_col < 0 or new_col >= n:
                    # exit
                    timelines += count
                else:
                    next_ways[new_col] = next_ways.get(new_col, 0) + count

        ways = next_ways

    timelines += sum(ways.values())
    return timelines


with open("07.input", "r") as file:
    din: str = file.read()

matrix_lines = din.strip().split("\n")
m: int = len(matrix_lines)
n: int = len(matrix_lines[0])

matrix = Matrix([m, n], default=".")

for i in range(m):
    for j in range(n):
        matrix[[i, j]] = matrix_lines[i][j]

p1_start: float = perf_counter()
print(f"Part One: {part1(matrix)}")
p1_end: float = perf_counter()
p1_elapsed: float = p1_end - p1_start

p2_start: float = perf_counter()
print(f"Part Two: {part2(matrix)}")
p2_end: float = perf_counter()
p2_elapsed: float = p2_end - p2_start

print(f"Elapsed Time (Part One): {p1_elapsed:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_elapsed:0.2f}s")