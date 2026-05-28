# Installation

## Requirements

- Python 3.10 or newer.

## Install from PyPI

```bash
pip install signtraker
```

## Optional extras

Enable `.env` loading via `python-dotenv`:

```bash
pip install "signtraker[dotenv]"
```

## Development install

```bash
git clone https://github.com/theperrygroup/signtraker.git
cd signtraker
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pip install -r docs/requirements.txt
```

## Verify

```python
import signtraker

print(signtraker.__version__)
```
