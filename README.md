# Adjutant

Python tool for source code generation and processing.

## Installation

Requires Python3 and Make.

## Usage

To process single file use command:

```
adjutant src/header.h -t src/_templates -o build/adj
```

## Development

Development setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 setup.py develop
```
