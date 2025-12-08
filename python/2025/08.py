from time import perf_counter
from math import prod


def parse_input(din: str) -> list[tuple[int, int, int]]:
    points = []
    for line in din.strip().splitlines():
        if not line:
            continue
        x, y, z = map(int, line.split(","))
        points.append((x, y, z))
    return points


def compute_edges(points):
    """sort by distance"""
    edges = []
    n = len(points)

    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist2 = dx*dx + dy*dy + dz*dz
            edges.append((dist2, i, j))

    edges.sort(key=lambda e: e[0])
    return edges


def merge_components(components, a, b):
    ca = components[a]
    cb = components[b]

    if ca == cb:
        return False

    for i in range(len(components)):
        if components[i] == cb:
            # merge
            components[i] = ca
    return True


def part1(points, edges, connections=1000):
    n = len(points)
    components = list(range(n))

    for k in range(connections):
        _, i, j = edges[k]
        merge_components(components, i, j)

    sizes = {}
    for c in components:
        sizes[c] = sizes.get(c, 0) + 1

    top3 = sorted(sizes.values(), reverse=True)[:3]
    while len(top3) < 3:
        top3.append(1)

    return prod(top3)


def part2(points, edges):
    n = len(points)
    components = list(range(n))
    comp_count = n

    last_merge_pair = None
    for dist2, i, j in edges:
        merged = merge_components(components, i, j)
        if merged:
            comp_count -= 1
            last_merge_pair = (i, j)

            if comp_count == 1:
                # everyting connected
                break

    i, j = last_merge_pair
    return points[i][0] * points[j][0]


if __name__ == "__main__":
    with open("08.input", "r") as file:
        din = file.read()

    points = parse_input(din)
    edges = compute_edges(points)

    p1_start = perf_counter()
    r1 = part1(points, edges)
    p1_end = perf_counter()

    p2_start = perf_counter()
    r2 = part2(points, edges)
    p2_end = perf_counter()

    print(f"Part One: {r1}")
    print(f"Part Two: {r2}")
    print(f"Elapsed P1: {p1_end - p1_start:0.2f}s")
    print(f"Elapsed P2: {p2_end - p2_start:0.2f}s")