from pathlib import Path


STEP = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1),
}

BACK = {"N": "S", "S": "N", "W": "E", "E": "W"}

LINKS = {
    "|": {"N", "S"},
    "-": {"W", "E"},
    "L": {"N", "E"},
    "J": {"N", "W"},
    "7": {"S", "W"},
    "F": {"S", "E"},
}


def solve(text):
    grid = [line for line in text.splitlines() if line]
    h, w = len(grid), len(grid[0])

    start = None
    for r in range(h):
        c = grid[r].find("S")
        if c != -1:
            start = (r, c)
            break
    if start is None:
        raise ValueError("Start tile 'S' was not found")

    def neighbors(r, c):
        ch = grid[r][c]
        if ch == "S":
            dirs = STEP.keys()
        elif ch in LINKS:
            dirs = LINKS[ch]
        else:
            return []

        out = []
        for d in dirs:
            dr, dc = STEP[d]
            nr, nc = r + dr, c + dc
            if not (0 <= nr < h and 0 <= nc < w):
                continue
            other = grid[nr][nc]
            if other == "S" or (other in LINKS and BACK[d] in LINKS[other]):
                out.append((nr, nc))
        return out

    first_steps = neighbors(start[0], start[1])
    if len(first_steps) != 2:
        raise ValueError("'S' must have exactly two neighbors in the main loop")

    loop_path = [start]
    prev = start
    cur = first_steps[0]
    while cur != start:
        loop_path.append(cur)
        options = neighbors(cur[0], cur[1])
        if len(options) != 2:
            raise ValueError("Each loop tile must have exactly two connections")
        nxt = options[0] if options[0] != prev else options[1]
        prev, cur = cur, nxt

    loop_cells = set(loop_path)
    part1 = len(loop_path) // 2

    dirs = []
    for nr, nc in first_steps:
        dr = nr - start[0]
        dc = nc - start[1]
        if dr == -1 and dc == 0:
            dirs.append("N")
        elif dr == 1 and dc == 0:
            dirs.append("S")
        elif dr == 0 and dc == -1:
            dirs.append("W")
        elif dr == 0 and dc == 1:
            dirs.append("E")

    s_key = "".join(sorted(dirs))
    s_shape = {
        "NS": "|",
        "EW": "-",
        "EN": "L",
        "NW": "J",
        "SW": "7",
        "ES": "F",
    }.get(s_key)
    if s_shape is None:
        raise ValueError("Could not resolve the pipe shape for 'S'")

    part2 = 0
    for r in range(h):
        inside = False
        open_corner = None
        for c in range(w):
            if (r, c) not in loop_cells:
                if inside:
                    part2 += 1
                continue

            tile = s_shape if (r, c) == start else grid[r][c]
            if tile == "|":
                inside = not inside
            elif tile in ("F", "L"):
                open_corner = tile
            elif tile in ("J", "7"):
                if (open_corner, tile) in (("F", "J"), ("L", "7")):
                    inside = not inside
                open_corner = None

    return part1, part2


if __name__ == "__main__":
    input_path = Path(__file__).with_name("puzzle_input.txt")
    part1_result, part2_result = solve(input_path.read_text(encoding="utf-8"))
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")
