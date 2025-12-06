from time import perf_counter


def parse_input(din: str) -> tuple[list[tuple[int, int]], list[int]]:
    blocks = din.strip().split("\n\n")
    range_block = blocks[0].strip().splitlines()
    id_block = blocks[1].strip().splitlines() if len(blocks) > 1 else []

    ranges: list[tuple[int, int]] = []
    for line in range_block:
        lo, hi = map(int, line.split("-"))
        ranges.append((lo, hi))

    ids: list[int] = [int(line) for line in id_block if line.strip()]
    return ranges, ids


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []

    # Sort by start
    ranges.sort(key=lambda r: r[0])
    merged = []
    cur_lo, cur_hi = ranges[0]

    for lo, hi in ranges[1:]:
        if lo <= cur_hi:  # Overlaps or touches
            cur_hi = max(cur_hi, hi)
        else:
            merged.append((cur_lo, cur_hi))
            cur_lo, cur_hi = lo, hi

    merged.append((cur_lo, cur_hi))
    return merged


def part1(ranges: list[tuple[int, int]], ids: list[int]) -> int:
    fresh = 0
    for ingredient_id in ids:
        for lo, hi in ranges:
            if lo <= ingredient_id <= hi:
                fresh += 1
                break
    return fresh


def part2(ranges: list[tuple[int, int]], ids: list[int]) -> int:
    merged = merge_ranges(ranges)
    total = 0
    for lo, hi in merged:
        total += hi - lo + 1
    return total


with open("05.input", "r") as file:
    din: str = file.read()

ranges, ids = parse_input(din)

p1_start = perf_counter()
print(f"Part One: {part1(ranges, ids)}")
p1_end = perf_counter()

p2_start = perf_counter()
print(f"Part Two: {part2(ranges, ids)}")
p2_end = perf_counter()

print(f"Elapsed Time (Part One): {p1_end - p1_start:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p2_start:0.2f}s")