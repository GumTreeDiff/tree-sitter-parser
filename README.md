# tree-sitter-parser

`tree-sitter-parser` is a GumTree wrapper for tree-sitter parsers. It conveniently converts source code files to XML files compatible with GumTree.

## Installation

First, install tree-sitter [Python's bindings](https://github.com/tree-sitter/py-tree-sitter): `pip3 install -r requirements.txt`. Then place `tree-sitter-parser.py` in your system's path.

To retrieve a GumTree XML run the command: `tree-sitter-parser.py FILE LANGUAGE` where `LANGUAGE` is the parser corresponding to `FILE` (for instance, `python`).

## Usage

The following command will write an AST XML on the standard output:

```
tree-sitter-parser.py FILE LANGUAGE
```

You can use the `--raw` option to deactivate the rewrite rules and the `--pretty` option to have a readable output instead of XML for debugging purpose.

## Rules

The resulting ASTs produced by the tree-sitter parsers can be fine-tuned using simple tree rewriting operations as defined in the `rules.yml` YAML file. There are three kinds of operations:
- `flattened` nodes: nodes for which the children won't be visited,
- `aliased` nodes: nodes that will be given a user-defined type,
- `ignored` nodes: nodes that will be ignored (as well as their children).

Here is an extract of the configuration for the Java language:

```
java:
  flattened:
    - integral_type
    - array_type
    - generic_type
  aliased:
    '&&': logical_operator
    '||': logical_operator
  ignored: 
    - ;
```

Currently, we only have a working configuration for Java. Don't hesitate to provide us with configurations for the other parsers via pull-requests.

## Grammars

Here is the list of the available parsers:
- `c`
- `c-sharp`
- `java`
- `javascript`
- `ocaml`
- `php`
- `python`
- `r`
- `ruby`
- `rust`
- `typescript`
