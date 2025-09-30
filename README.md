# AutoRefactor (Python) — local-first refactoring assistant

AutoRefactor helps you find small, high-impact refactors in Python code safely and locally.

## Features
- Detects nested loops
- Suggests `for i, v in enumerate()` instead of `range(len(...))`
- Detects `list.count()` usage for better performance
- Optional `rich` CLI output for prettier terminal output
- Non-destructive `.refactored` files for review before overwriting

## Quick Start

### Create & activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```
Run analyzer
```
python -m autorefactor.cli examples/messy_example.py
```
Write conservative, reviewable refactors
```
python -m autorefactor.cli examples/messy_example.py --apply
```
Example Before / After

Before:
```
for i in range(len(items)):
    print(items[i])
```
After (candidate .refactored):
```
for i, __val in enumerate(items):
    print(__val)
```
Contributing

    Add new rule modules under autorefactor/ (prefix: rules_)

    Add tests for each new rule under tests/

    Keep commits small and humanly descriptive

    Label easy issues with good first issue to attract contributors

License

MIT License

Built locally by Howard-Dominic. Open to contributions and ideas!
