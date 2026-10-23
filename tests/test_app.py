import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def test_home_page_lists_every_function_with_a_try_button(client):
    response = client.get("/")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert page.count('class="try-button"') == 16
    assert 'id="function-form"' in page
    assert 'id="output"' in page


@pytest.mark.parametrize(
    ("function", "arguments", "expected"),
    [
        ("is_adult", [18], True),
        ("celsius_to_fahrenheit", [0], 32.0),
        ("count_vowels", ["Hello"], 2),
        ("invert", [True], False),
        ("greet", [None], "Hello, Guest!"),
        ("find_max", [[1, 4, 2]], 4),
        ("get_price", [{"book": 4.5}, "book"], 4.5),
        ("swap", [[1, "two"]], ["two", 1]),
        ("common_items", [[1, 2, 3], [2, 3, 4]], [2, 3]),
        ("is_leap_year", [2000], True),
        ("to_int", ["42"], 42),
        ("divide", [8, 2], 4.0),
        ("power", [2, 3], 8),
        ("square_root", [81], 9.0),
        ("factorial", [5], 120),
        ("average", [[1, 2, 3]], 2.0),
    ],
)
def test_run_executes_each_target_function(client, function, arguments, expected):
    response = client.post(
        "/run",
        json={"function": function, "arguments": arguments},
    )

    assert response.status_code == 200
    assert response.json["result"] == expected


def test_run_returns_function_errors_to_the_frontend(client):
    response = client.post(
        "/run",
        json={"function": "divide", "arguments": [1, 0]},
    )

    assert response.status_code == 400
    assert response.json["error"] == {
        "type": "ZeroDivisionError",
        "message": "cannot divide by zero",
    }


@pytest.mark.parametrize(
    ("payload", "expected_type"),
    [
        ({"function": "unknown", "arguments": []}, "InvalidFunction"),
        ({"function": "greet", "arguments": "Ada"}, "InvalidArguments"),
        (["greet", ["Ada"]], "InvalidRequest"),
    ],
)
def test_run_rejects_invalid_requests(client, payload, expected_type):
    response = client.post("/run", json=payload)

    assert response.status_code == 400
    assert response.json["error"]["type"] == expected_type


def test_run_reports_invalid_json_request(client):
    response = client.post(
        "/run",
        data="{invalid",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json["error"]["type"] == "InvalidRequest"
