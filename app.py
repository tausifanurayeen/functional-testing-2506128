import os
import re
import subprocess

from flask import Flask, jsonify, render_template, request

from target import (
    average,
    common_items,
    count_vowels,
    celsius_to_fahrenheit,
    divide,
    factorial,
    find_max,
    get_price,
    greet,
    invert,
    is_adult,
    is_leap_year,
    power,
    square_root,
    swap,
    to_int,
)

app = Flask(__name__)
COMMIT_SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")

FUNCTIONS = {
    "is_adult": is_adult,
    "celsius_to_fahrenheit": celsius_to_fahrenheit,
    "count_vowels": count_vowels,
    "invert": invert,
    "greet": greet,
    "find_max": find_max,
    "get_price": get_price,
    "swap": swap,
    "common_items": common_items,
    "is_leap_year": is_leap_year,
    "to_int": to_int,
    "divide": divide,
    "power": power,
    "square_root": square_root,
    "factorial": factorial,
    "average": average,
}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    commit_sha = os.environ.get("APP_COMMIT_SHA")
    if commit_sha is None:
        try:
            commit_sha = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=app.root_path,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        except (FileNotFoundError, subprocess.CalledProcessError):
            return (
                jsonify(
                    error="Commit SHA is unavailable; set APP_COMMIT_SHA at deploy time."
                ),
                503,
            )

    if not COMMIT_SHA_PATTERN.fullmatch(commit_sha):
        return jsonify(error="APP_COMMIT_SHA must be a full 40-character commit SHA."), 503

    return jsonify(sha=commit_sha)


@app.post("/run")
def run_function():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return (
            jsonify(error={"type": "InvalidRequest", "message": "Send a JSON object."}),
            400,
        )

    function_name = payload.get("function")
    if not isinstance(function_name, str) or function_name not in FUNCTIONS:
        return (
            jsonify(
                error={
                    "type": "InvalidFunction",
                    "message": "Choose a supported function.",
                }
            ),
            400,
        )

    arguments = payload.get("arguments")
    if not isinstance(arguments, list):
        return (
            jsonify(
                error={
                    "type": "InvalidArguments",
                    "message": "Arguments must be a JSON array.",
                }
            ),
            400,
        )

    if function_name == "common_items":
        if any(not isinstance(argument, list) for argument in arguments):
            return (
                jsonify(
                    error={
                        "type": "InvalidArguments",
                        "message": "common_items expects two JSON arrays.",
                    }
                ),
                400,
            )

    try:
        if function_name == "common_items":
            arguments = [set(argument) for argument in arguments]
        result = FUNCTIONS[function_name](*arguments)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        return (
            jsonify(
                error={"type": type(error).__name__, "message": str(error)}
            ),
            400,
        )

    result_type = type(result).__name__
    if isinstance(result, set):
        result = sorted(result, key=repr)
    elif isinstance(result, tuple):
        result = list(result)
    elif isinstance(result, complex):
        result = repr(result)

    return jsonify(result=result, result_type=result_type)


if __name__ == "__main__":
    app.run()
