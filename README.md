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

## Run the frontend

Start the Flask app and open `http://127.0.0.1:5000` in a browser. Choose a
function, provide its positional arguments as a JSON array, and select **Run
function**. The `common_items` function accepts JSON arrays for its set inputs.
The page also displays the deployed commit SHA from `/health`. Set
`APP_COMMIT_SHA` to the full 40-character commit SHA in deployment environments.
On Render, the app reads `RENDER_GIT_COMMIT`; locally, it reads the current SHA
from Git.

```bash
python app.py
```

## Deploy to Render

Create a Render **Web Service** for this GitHub repository using the `main`
branch. Use these settings:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --bind 0.0.0.0:$PORT app:app`
- Disable Render's automatic deploys so deployments are gated by GitHub Actions.

In GitHub, add the Render deploy hook URL as the `RENDER_DEPLOY_HOOK_URL`
repository Actions secret, and add the public service URL (for example,
`https://your-service.onrender.com`) as the `LIVE_URL` repository variable.
After that, pushes to `main` run the test matrix, trigger the Render deploy for
that exact commit, wait for `/health` to report its SHA, and check the homepage,
health endpoint, and function runner.
