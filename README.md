# Adjutant

Python tool for source code generation and processing.

## Installation

Requires Python3 and Make.

## Usage

In your source code directory use init command to create configuration file:

```bash
adjutant init
```

Setup will ask you where to look for source files and where to perform build.

To build your project use:

```bash
adjutant build
```

## Development

Development setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 setup.py develop
```
