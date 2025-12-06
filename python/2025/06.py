from time import perf_counter
from lib.matrix import Matrix


def _build_blocks(matrix: Matrix) -> list[tuple[int, int]]:
    height, width = matrix.size

    empty_cols: list[bool] = []
    for col in range(width):
        col_chars = [matrix[[row, col]] for row in range(height)]
        empty_cols.append(all(c == ' ' for c in col_chars))

    blocks: list[tuple[int, int]] = []
    in_block = False
    start = 0
    for col in range(width):
        if not empty_cols[col] and not in_block:
            in_block = True
            start = col
        if empty_cols[col] and in_block:
            in_block = False
            blocks.append((start, col - 1))
    if in_block:
        blocks.append((start, width - 1))

    return blocks


def _build_rows(matrix: Matrix) -> list[str]:
    height, width = matrix.size
    return ["".join(matrix[[i, j]] for j in range(width)) for i in range(height)]


def _extract_operator(block_rows: list[str], idx) -> str:
    op_chars = [ch for ch in block_rows[idx] if ch in "+*"]
    return op_chars[0]


def _eval_block_part1(block_rows: list[str]) -> int:
    op_row_index = len(block_rows) - 1
    operator = _extract_operator(block_rows, op_row_index)

    number_rows = block_rows[:op_row_index]
    numbers: list[int] = []
    for r in number_rows:
        stripped = r.strip()
        if stripped.isdigit():
            numbers.append(int(stripped))

    if operator == '+':
        return sum(numbers)

    result = 1
    for x in numbers:
        result *= x
    return result


def _eval_block_part2(block_rows: list[str]) -> int:
    op_row_index = len(block_rows) - 1
    operator = _extract_operator(block_rows, op_row_index)

    height = op_row_index          # rows 0..op_row_index-1 contain digits/space
    width = len(block_rows[0])     # block width in characters

    numbers: list[int] = []
    for col in range(width - 1, -1, -1):
        digits: list[str] = []
        for row in range(height):
            ch = block_rows[row][col]
            if ch.isdigit():
                digits.append(ch)
        if digits:
            num = int("".join(digits))
            numbers.append(num)

    if operator == '+':
        return sum(numbers)

    result = 1
    for x in numbers:
        result *= x
    return result


def part1(matrix: Matrix) -> int:
    rows = _build_rows(matrix)
    blocks = _build_blocks(matrix)

    total = 0
    for c0, c1 in blocks:
        block_rows = [row[c0:c1 + 1] for row in rows]
        total += _eval_block_part1(block_rows)

    return total


def part2(matrix: Matrix) -> int:
    rows = _build_rows(matrix)
    blocks = _build_blocks(matrix)

    total = 0
    for c0, c1 in blocks:
        block_rows = [row[c0:c1 + 1] for row in rows]
        total += _eval_block_part2(block_rows)

    return total


with open('06.input', 'r') as file:
    din: str = file.read()

matrix_lines = din.split('\n')
height: int = len(matrix_lines)
width: int = max(len(line) for line in matrix_lines)

matrix = Matrix([height, width], default=' ')

for i in range(height):
    line = matrix_lines[i]
    for j in range(len(line)):
        matrix[[i, j]] = line[j]

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