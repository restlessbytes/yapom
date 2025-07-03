import pytest

import yapom.utils as utils


@pytest.mark.parametrize(
    "runtime, format_str",
    [
        (0, ""),
        (1, "1s"),
        (300, "5m"),
        (605, "10m5s"),
        (3600, "1h"),
    ],
)
def test_runtime_formatting(runtime, format_str):
    assert utils.format_runtime(runtime) == format_str


@pytest.mark.parametrize(
    "input_string, expected_runtime",
    [
        ("", 0),
        ("1s", 1),
        ("1m", 60),
        ("1h", 3600),
        ("42s", 42),
        ("25m", 1500),
        ("10h", 36_000),
        ("3h42m5s", 13_325),
        # NOTE Integers without temporal unit will be interpreted as 'seconds'
        ("1", 1),
        ("10", 10),
    ],
)
def test_runtime_from_string(input_string: str, expected_runtime: int):
    assert utils.runtime_from_string(input_string) == expected_runtime
