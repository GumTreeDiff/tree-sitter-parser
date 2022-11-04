# tree-sitter-parser

This is a GumTree wrapper towards tree-sitter grammars. It conveniently converts source code file to XML files compatible with GumTree.

## Installation

First, install tree-sitter [Python's bindings](https://github.com/tree-sitter/py-tree-sitter): `pip3 install -r requirements.txt`. Then place `tree-sitter-parser.py` in your system's path.

To retrieve a GumTree XML run the command : `tree-sitter-parser.py FILE LANGUAGE`. Where `LANGUAGE` is the grammar corresponding to `FILE` (for instance `python`).