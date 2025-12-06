from time import perf_counter


def _generate_invalid_ids_exact_twice(min_id: int, max_id: int) -> list[int]:
    """
    Part 1: numbers of the form T T (exactly two repeats).
    Examples: 11, 55, 6464, 123123.
    """
    invalid_ids: list[int] = []
    max_len: int = len(str(max_id))

    # Only even total lengths can be of the form T + T
    for total_len in range(2, max_len + 1, 2):
        half_len: int = total_len // 2
        # T cannot have leading zero
        start_prefix: int = 10 ** (half_len - 1)
        end_prefix: int = 10**half_len

        for prefix in range(start_prefix, end_prefix):
            s = str(prefix)
            val = int(s + s)
            if val > max_id:
                # For fixed length and increasing prefix, val is strictly increasing
                break
            if val >= min_id:
                invalid_ids.append(val)

    invalid_ids.sort()
    return invalid_ids


def _generate_invalid_ids_at_least_twice(min_id: int, max_id: int) -> list[int]:
    """
    Part 2: numbers of the form T repeated k times, with k >= 2.
    Examples: 12341234 (1234 x2), 123123123 (123 x3),
              1212121212 (12 x5), 1111111 (1 x7).
    """
    invalid_ids_set: set[int] = set()
    max_len: int = len(str(max_id))

    # Total length must be at least 2 digits (1 digit repeated twice)
    for total_len in range(2, max_len + 1):
        # total_len = len(T) * k, with k >= 2
        for k in range(2, total_len + 1):
            if total_len % k != 0:
                continue
            half_len: int = total_len // k
            # T cannot start with '0'
            start_prefix: int = 10 ** (half_len - 1)
            end_prefix: int = 10**half_len

            for prefix in range(start_prefix, end_prefix):
                s = str(prefix)
                val_str = s * k
                val = int(val_str)
                if val > max_id:
                    # For fixed (total_len, k) and increasing prefix, val increases monotonically
                    break
                if val >= min_id:
                    invalid_ids_set.add(val)

    invalid_ids: list[int] = sorted(invalid_ids_set)
    return invalid_ids


def _sum_invalid_in_ranges(invalid_ids: list[int]) -> int:
    """
    Given sorted invalid_ids, sum each invalid ID once if it lies
    within ANY of the ID_RANGES (union semantics across ranges).
    """
    ranges_sorted = sorted(ID_RANGES)
    total: int = 0
    r_idx: int = 0
    num_ranges: int = len(ranges_sorted)

    for val in invalid_ids:
        # Advance range index while current range ends before val
        while r_idx < num_ranges and ranges_sorted[r_idx][1] < val:
            r_idx += 1

        if r_idx == num_ranges:
            # No further ranges can contain larger vals
            break

        lo, hi = ranges_sorted[r_idx]
        if lo <= val <= hi:
            total += val

    return total


def part1() -> int:
    # Use globally parsed ID_RANGES; matrix is unused for this puzzle.
    min_id: int = min(lo for lo, _ in ID_RANGES)
    max_id: int = max(hi for _, hi in ID_RANGES)

    invalid_ids: list[int] = _generate_invalid_ids_exact_twice(min_id, max_id)
    return _sum_invalid_in_ranges(invalid_ids)


def part2() -> int:
    min_id: int = min(lo for lo, _ in ID_RANGES)
    max_id: int = max(hi for _, hi in ID_RANGES)

    invalid_ids: list[int] = _generate_invalid_ids_at_least_twice(min_id, max_id)
    return _sum_invalid_in_ranges(invalid_ids)


def _parse_ranges(raw: str) -> list[tuple[int, int]]:
    parts = [p.strip() for p in raw.strip().split(",") if p.strip()]
    ranges: list[tuple[int, int]] = []
    for p in parts:
        lo, hi = p.split("-")
        ranges.append((int(lo), int(hi)))
    return ranges


with open("02.input", "r") as file:
    din: str = file.read().strip()

ID_RANGES: list[tuple[int, int]] = _parse_ranges(din)


p1_start: float = perf_counter()
print(f"Part One: {part1()}")
p1_end: float = perf_counter()
p1_elapsed: float = p1_end - p1_start

p2_start: float = perf_counter()
print(f"Part Two: {part2()}")
p2_end: float = perf_counter()
p2_elapsed: float = p2_end - p2_start

print(f"Elapsed Time (Part One): {p1_elapsed:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_elapsed:0.2f}s")