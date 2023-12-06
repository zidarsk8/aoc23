import pytest
from icecream import ic
import math

test_text = """
Time:      7  15   30
Distance:  9  40  200
""".strip()

text = """
Time:        54     70     82     75
Distance:   239   1142   1295   1253
""".strip()


def parse_text(input):
    times, distances = input.splitlines()
    return [
        {"time": int(t), "distance": int(d)}
        for t, d in zip(times.split()[1:], distances.split()[1:])
    ]


def parse_text_2(input):
    times, distances = input.splitlines()
    return [
        {
            "time": int(times.split(":")[1].replace(" ", "")),
            "distance": int(distances.split(":")[1].replace(" ", "")),
        }
    ]


def f(t, i, d):
    return (t - i) * i - d


def bisect(l, r, t, d):
    n = (l + r) // 2
    while l < r - 1:
        n = (l + r) // 2
        if f(t, l, d) * f(t, n, d) > 0:
            l = n
        else:
            r = n

    times = {f(t, i, d): i for i in range(r - 2, r + 2) if f(t, i, d) > 0}
    return times[min(times)]


def calculate_range(t, d):
    # valid_times = [i for i in range(t) if f(t, i, d) > 0]
    left_index = bisect(0, t // 2, t, d)
    right_index = bisect(t // 2, t, t, d)
    return right_index - left_index + 1


@pytest.mark.parametrize(
    "time,distance,result",
    (
        (7, 9, 4),
        (15, 40, 8),
        (30, 200, 9),
    ),
)
def test_calculate_range(time, distance, result):
    assert calculate_range(time, distance) == result


def multiply_ranges(data):
    return math.prod(calculate_range(d["time"], d["distance"]) for d in data)


def test_part1():
    test_data = parse_text(test_text)
    assert multiply_ranges(test_data) == 288

    data = parse_text(text)
    assert multiply_ranges(data) == 800280


def test_part2():
    test_data = parse_text_2(test_text)
    assert multiply_ranges(test_data) == 71503

    data = parse_text_2(text)
    assert multiply_ranges(data) == 45128024


def test_parse_text_2():
    assert parse_text_2(test_text) == [
        {"time": 71530, "distance": 940200},
    ]
    assert parse_text_2(text) == [
        {"time": 54708275, "distance": 239114212951253},
    ]


def test_parse_text():
    assert parse_text(test_text) == [
        {"time": 7, "distance": 9},
        {"time": 15, "distance": 40},
        {"time": 30, "distance": 200},
    ]
    assert parse_text(text) == [
        {"time": 54, "distance": 239},
        {"time": 70, "distance": 1142},
        {"time": 82, "distance": 1295},
        {"time": 75, "distance": 1253},
    ]
