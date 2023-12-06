import pytest
from aoc05 import text, test_text, parse_input

Range = tuple[int, int]


def breakup_range(main_range: Range, splits: list[Range]) -> list[Range]:
    if not splits:
        return [main_range]

    if main_range[0] > splits[0][1]:
        return breakup_range(main_range, splits[1:])

    if main_range[1] < splits[0][0]:
        return [main_range]

    result = []
    if main_range[0] < splits[0][0]:
        result.append((main_range[0], splits[0][0] - 1))
        main_range = (splits[0][0], main_range[1])

    if main_range[1] <= splits[0][1]:
        result.append(main_range)
    else:
        result.append((main_range[0], splits[0][1]))
        main_range = (splits[0][1] + 1, main_range[1])
        result += breakup_range(main_range, splits[1:])

    return result


def translate_range(main_range, range_maps):
    for r in range_maps:
        if r[0][0] <= main_range[0] <= r[0][1]:
            diff = r[1][0] - r[0][0]
            return (main_range[0] + diff, main_range[1] + diff)
    return main_range


def translate_ranges(ranges, range_maps):
    splits = sorted([m[0] for m in range_maps])
    ranges = sum([breakup_range(r, splits) for r in ranges], [])
    return [translate_range(r, range_maps) for r in ranges]


def handle_text(text, steps=None):
    data = parse_input(text)
    seeds = data["seeds"]
    maps = data["maps"]
    if steps is None:
        steps = len(maps)

    base_ranges = [
        (seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)
    ]
    for i in range(steps):
        base_ranges = translate_ranges(base_ranges, sorted(maps[i]["ranges"]))
    return base_ranges


def test_handle_test_text():
    assert handle_text(test_text, 0) == [(79, 92), (55, 67)]
    assert handle_text(test_text, 1) == [(81, 94), (57, 69)]
    assert handle_text(test_text, 2) == [(81, 94), (57, 69)]
    assert handle_text(test_text, 3) == [(81, 94), (53, 56), (61, 69)]
    assert handle_text(test_text, 4) == [(74, 87), (46, 49), (54, 62)]
    assert min(min(handle_text(test_text))) == 46
    assert min(min(handle_text(text))) == 31161857


@pytest.mark.parametrize(
    "main_range, splits ,expected",
    [
        ((5, 2), [], (5, 2)),
        ((3, 6), [((0, 9), (10, 19))], (13, 16)),
        ((3, 6), [((3, 6), (5, 8))], (5, 8)),
        ((3, 6), [((3, 6), (1, 4))], (1, 4)),
        ((5, 6), [((3, 6), (1, 4))], (3, 4)),
    ],
)
def test_translate_range(main_range, splits, expected):
    assert translate_range(main_range, splits) == expected


@pytest.mark.parametrize(
    "main_range, splits ,expected",
    [
        ([(5, 2)], [], [(5, 2)]),
        (
            [(2, 6), (9, 11)],
            [
                ((0, 4), (10, 14)),
                ((5, 9), (1, 5)),
            ],
            [(12, 14), (1, 2), (5, 5), (10, 11)],
        ),
    ],
)
def test_translate_ranges(main_range, splits, expected):
    assert translate_ranges(main_range, splits) == expected


@pytest.mark.parametrize(
    "main_range, splits ,expected",
    [
        ((5, 2), [], [(5, 2)]),
        ((3, 6), [(0, 9)], [(3, 6)]),
        ((3, 6), [(3, 6)], [(3, 6)]),
        ((8, 9), [(3, 6)], [(8, 9)]),
        ((1, 2), [(3, 6)], [(1, 2)]),
        ((1, 5), [(3, 6)], [(1, 2), (3, 5)]),
        ((4, 7), [(3, 6)], [(4, 6), (7, 7)]),
        ((3, 6), [(3, 6), (9, 11)], [(3, 6)]),
        ((2, 6), [(3, 6), (9, 11)], [(2, 2), (3, 6)]),
        ((1, 3), [(3, 6), (9, 11)], [(1, 2), (3, 3)]),
        ((6, 7), [(3, 6), (9, 11)], [(6, 6), (7, 7)]),
        ((6, 9), [(3, 6), (9, 11)], [(6, 6), (7, 8), (9, 9)]),
        ((6, 9), [(3, 8), (9, 11)], [(6, 8), (9, 9)]),
        ((1, 16), [(3, 6), (9, 11)], [(1, 2), (3, 6), (7, 8), (9, 11), (12, 16)]),
    ],
)
def test_breakup_range(main_range, splits, expected):
    assert breakup_range(main_range, splits) == expected
