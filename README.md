# Adjutant

Python tool for source code generation and processing.

### How it works

Project configuration file (`adjutant.py`) contains list of rules, that specify what to look for in source code and in which files to look. 

Matched content is then sent to templates which generate new files.

## Installation

Requires Python3 and Make.

```bash
pip install git+git://github.com/bstjepanovic1/adjutant
```

## Usage

In your source code directory use init command to create configuration file:

```bash
adjutant initconfiguration
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
make install-develop
```
