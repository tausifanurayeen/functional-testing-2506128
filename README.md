# Functional Testing

[![CI](https://github.com/tausifanurayeen/functional-testing-2506128/actions/workflows/ci.yml/badge.svg)](https://github.com/tausifanurayeen/functional-testing-2506128/actions/workflows/ci.yml)

## Run tests locally

Install the pinned development dependencies and run the test suite with branch
coverage enforcement:

```bash
python -m pip install -r requirements.txt
python -m ruff check .
python -m pytest --cov=target --cov-branch --cov-report=term-missing --cov-fail-under=100
```
