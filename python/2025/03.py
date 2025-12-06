from time import perf_counter


def _max_k_subsequence_value(row: str, k: int) -> int:
    """
    Select exactly k digits (in order) to form the maximum lexicographic number.
    Classic greedy windowing approach.
    """
    n = len(row)
    res = []
    start = 0

    for pos in range(k):
        remaining = k - pos
        end = n - remaining

        best_digit = '0'
        best_idx = start

        for i in range(start, end + 1):
            d = row[i]
            if d > best_digit:
                best_digit = d
                best_idx = i
                if d == '9':
                    break

        res.append(best_digit)
        start = best_idx + 1

    return int("".join(res))



def part1(banks: list[str], K: int = 2) -> int:
    total = 0
    for row in banks:
        total += _max_k_subsequence_value(row, K)
    return total


def part2(banks: list[str], K: int = 12) -> int:
    total = 0
    for row in banks:
        total += _max_k_subsequence_value(row, K)
    return total


with open('03.input', 'r') as f:
    banks = f.read().strip().split('\n')

p1_start = perf_counter()
print(f"Part One: {part1(banks)}")
p1_end = perf_counter()

p2_start = perf_counter()
print(f"Part Two: {part2(banks)}")
p2_end = perf_counter()

print(f"Elapsed Time (Part One): {p1_end - p1_start:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p2_start:0.2f}s")