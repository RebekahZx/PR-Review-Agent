# PR Review Agent (v1)

> **This is the first version.** The current project, with retrieval-augmented review, a GitHub
> webhook, tests and CI, is **[RebekahZx/pr](https://github.com/RebekahZx/pr)**. This repo is kept
> to show where it started.

A Flask web app that reviews a GitHub pull request with an LLM. Paste a repo URL and a PR number,
and it fetches each changed file's diff, sends it to Gemini (`gemini-2.5-flash`), and shows a
review per file covering readability, bugs and style.

## How it works

```
web form (repo URL + PR number)
        │
        ▼
review_engine/pr_fetcher.py     fetch changed files and patches (PyGithub)
        │
        ▼
review_engine/ai_reviewer.py    split each patch into 200-line chunks → one Gemini call per chunk
        │
        ▼
templates/index.html            show the combined feedback for each file
```

There is also a **rule-based command-line mode** (`main.py` → `review_engine/reviewer.py`) that
needs no LLM. It flags:

- PRs that add more than 200 lines;
- leftover `print(` calls;
- `TODO`/`FIXME` comments;
- files with no real changes.

## Run

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=...      # Google AI Studio key
export GITHUB_TOKEN=...        # read access to the repository under review
python app.py                  # http://127.0.0.1:5000
```

Rule-based CLI:

```bash
python main.py --token "$GITHUB_TOKEN" --repo owner/repo --pr 12
```

Credentials are read from the environment only.

## Limitations, and what v2 changed

- **No codebase context.** v1 reviews only the diff text, so the model can't see the functions a
  change calls or the code it affects. v2 retrieves related code from the repository before
  reviewing. This is the main difference.
- **Arbitrary chunk boundaries.** Patches are cut every 200 lines, which can split a function in
  half. v2 chunks code at function and class boundaries with tree-sitter.
- **GitHub only.** `gitlab_fetcher.py` and `bitbucket_fetcher.py` are early stubs, and the web app
  doesn't use them.
- **Manual and untested.** v1 is run by hand and has no tests. v2 runs from a GitHub webhook,
  verifies the webhook signature, and has an offline test suite with CI.

## Author

Shrinivas Anavekar
