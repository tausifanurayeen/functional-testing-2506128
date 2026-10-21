import pytest

from target import (
    common_items,
    count_vowels,
    celsius_to_fahrenheit,
    find_max,
    get_price,
    greet,
    invert,
    is_adult,
    is_leap_year,
    swap,
    to_int,
)


@pytest.mark.parametrize(
    ("age", "expected"),
    [(0, False), (17, False), (18, True), (65, True)],
)
def test_is_adult(age, expected):
    assert is_adult(age) is expected


def test_is_adult_rejects_negative_age():
    with pytest.raises(ValueError, match="age cannot be negative"):
        is_adult(-1)


@pytest.mark.parametrize(
    ("celsius", "expected"),
    [(0, 32.0), (100, 212.0), (-40, -40.0), (37.78, 100.0)],
)
def test_celsius_to_fahrenheit(celsius, expected):
    result = celsius_to_fahrenheit(celsius)

    assert isinstance(result, float)
    assert result == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Functional testing", 6),
        ("AEIOU aeiou", 10),
        ("rhythm", 0),
        ("", 0),
    ],
)
def test_count_vowels(text, expected):
    assert count_vowels(text) == expected


def test_count_vowels_rejects_non_string():
    with pytest.raises(TypeError, match="text must be a string"):
        count_vowels(123)


@pytest.mark.parametrize(("flag", "expected"), [(True, False), (False, True)])
def test_invert(flag, expected):
    result = invert(flag)

    assert isinstance(result, bool)
    assert result is expected


def test_invert_rejects_non_boolean():
    with pytest.raises(TypeError, match="flag must be True or False"):
        invert(1)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        (None, "Hello, Guest!"),
        ("", "Hello, Guest!"),
        ("   ", "Hello, Guest!"),
        ("Ada", "Hello, Ada!"),
        ("  Ada Lovelace  ", "Hello, Ada Lovelace!"),
    ],
)
def test_greet(name, expected):
    assert greet(name) == expected


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [([1, 3, 2], 3), ([-5, -2, -9], -2), ([4], 4)],
)
def test_find_max(numbers, expected):
    assert find_max(numbers) == expected


def test_find_max_rejects_empty_list():
    with pytest.raises(ValueError, match="list is empty"):
        find_max([])


def test_get_price_returns_matching_item_price():
    assert get_price({"book": 12.5, "pen": 2.0}, "book") == 12.5


def test_get_price_rejects_missing_item():
    with pytest.raises(KeyError, match="missing not found"):
        get_price({"book": 12.5}, "missing")


@pytest.mark.parametrize(
    ("pair", "expected"),
    [((1, "two"), ("two", 1)), (("same", "same"), ("same", "same"))],
)
def test_swap(pair, expected):
    result = swap(pair)

    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.parametrize("pair", [(), (1,), (1, 2, 3)])
def test_swap_rejects_pairs_with_wrong_length(pair):
    with pytest.raises(ValueError, match="pair must have exactly 2 values"):
        swap(pair)


@pytest.mark.parametrize(
    ("set_a", "set_b", "expected"),
    [
        ({1, 2, 3}, {2, 3, 4}, {2, 3}),
        (set(), {1}, set()),
        ({1}, {2}, set()),
    ],
)
def test_common_items(set_a, set_b, expected):
    result = common_items(set_a, set_b)

    assert isinstance(result, set)
    assert result == expected


@pytest.mark.parametrize(
    ("year", "expected"),
    [(2000, True), (1900, False), (2024, True), (2023, False), (4, True)],
)
def test_is_leap_year(year, expected):
    assert is_leap_year(year) is expected


def test_is_leap_year_rejects_year_below_one():
    with pytest.raises(ValueError, match="year must be 1 or more"):
        is_leap_year(0)


@pytest.mark.parametrize(
    ("value", "expected"),
    [(42, 42), ("42", 42), (3.9, 3), ("-7", -7)],
)
def test_to_int(value, expected):
    result = to_int(value)

    assert isinstance(result, int)
    assert result == expected


def test_to_int_rejects_boolean():
    with pytest.raises(TypeError, match="bool is not allowed"):
        to_int(True)
