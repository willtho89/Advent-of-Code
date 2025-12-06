from time import perf_counter


def parse(din: str) -> list[tuple[str, int]]:
    rotations: list[tuple[str, int]] = []
    for line in din.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        direction: str = line[0]
        distance: int = int(line[1:])
        rotations.append((direction, distance))
    return rotations


def part1(din: str) -> int:
    rotations = parse(din)

    position: int = 50
    hits_zero: int = 0

    for direction, distance in rotations:
        if direction == "L":
            position = (position - distance) % 100
        else:  # "R"
            position = (position + distance) % 100

        if position == 0:
            hits_zero += 1

    return hits_zero


def _count_hits_and_advance(start: int, direction: str, distance: int) -> tuple[int, int]:
    """
    Return (end_position, hits_at_zero) for a single rotation, counting
    every click where the dial points at 0.
    Dial has values 0..99, moves 1 per click, wrapping.
    """
    if distance <= 0:
        return start, 0

    if direction == "R":
        # Need k in [1, distance] with (start + k) % 100 == 0
        base: int = (100 - start) % 100
    else:  # "L"
        # Need k in [1, distance] with (start - k) % 100 == 0 -> k ≡ start (mod 100)
        base = start % 100

    if base == 0:
        first_hit: int = 100  # first positive k satisfying k ≡ 0 (mod 100)
    else:
        first_hit = base

    if first_hit > distance:
        hits: int = 0
    else:
        hits = 1 + (distance - first_hit) // 100

    if direction == "R":
        end: int = (start + distance) % 100
    else:
        end = (start - distance) % 100

    return end, hits


def part2(din: str) -> int:
    rotations = parse(din)

    position: int = 50
    hits_zero: int = 0

    for direction, distance in rotations:
        position, hits = _count_hits_and_advance(position, direction, distance)
        hits_zero += hits

    return hits_zero


with open("01.input", "r") as file:
    din: str = file.read()

p1_start: float = perf_counter()
print(f"Part One: {part1(din)}")
p1_end: float = perf_counter()
p1_elapsed: float = p1_end - p1_start

p2_start: float = perf_counter()
print(f"Part Two: {part2(din)}")
p2_end: float = perf_counter()
p2_elapsed: float = p2_end - p2_start

print(f"Elapsed Time (Part One): {p1_elapsed:0.6f}s")
print(f"Elapsed Time (Part Two): {p2_elapsed:0.6f}s")