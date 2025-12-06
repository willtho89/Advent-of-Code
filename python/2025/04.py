from time import perf_counter
from lib.matrix import Matrix

ADJ8: list[tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def _count_adjacent_rolls(matrix: Matrix, i: int, j: int) -> int:
    """Count adjacent '@' in the 8-neighborhood for cell (i, j)."""
    count: int = 0
    for di, dj in ADJ8:
        ni, nj = i + di, j + dj
        if matrix._is_in_bounds([ni, nj]) and matrix[[ni, nj]] == '@':
            count += 1
    return count


def part1(matrix: Matrix) -> int:
    """Number of rolls accessible in the initial configuration."""
    total: int = 0

    for i in range(m):
        for j in range(n):
            if matrix[[i, j]] != '@':
                continue

            if _count_adjacent_rolls(matrix, i, j) < 4:
                total += 1

    return total


def part2(matrix: Matrix) -> int:
    """
    Iteratively remove all accessible rolls.

    In each round:
      - Determine all '@' with < 4 adjacent '@'
      - Remove them simultaneously
      - Repeat until no more '@' are accessible
    Return total number of removed rolls.
    """

    # Reset matrix to original state (in case part1 or other code mutated it later).
    for i in range(m):
        for j in range(n):
            matrix[[i, j]] = matrix_lines[i][j]

    removed_total: int = 0

    while True:
        to_remove: list[tuple[int, int]] = []

        # Find all accessible rolls in the current state.
        for i in range(m):
            for j in range(n):
                if matrix[[i, j]] != '@':
                    continue
                if _count_adjacent_rolls(matrix, i, j) < 4:
                    to_remove.append((i, j))

        # No more accessible rolls -> stop.
        if not to_remove:
            break

        # Remove all accessible rolls simultaneously.
        for i, j in to_remove:
            matrix[[i, j]] = '.'

        removed_total += len(to_remove)

    return removed_total


with open('04.input', 'r') as file:
    din: str = file.read()

matrix_lines = din.strip().split('\n')
m: int = len(matrix_lines)
n: int = len(matrix_lines[0])

matrix = Matrix([m, n], default='.')

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