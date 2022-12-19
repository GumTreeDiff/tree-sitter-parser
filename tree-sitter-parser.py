#!/usr/bin/env python3

import argparse
import os
from io import StringIO

import yaml
from tree_sitter_parser import (
    EMPTY_CONFIG,
    init_parsers,
    parse_and_translate,
    pretty_print_ast,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="path to the file to parse")
    parser.add_argument("language", help="language of to the file to parse")
    parser.add_argument(
        "--raw", action="store_true", help="deactivate the rewrite rules"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="pretty print the AST instead of using XML",
    )
    args = parser.parse_args()

    script_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    rules_file = (
        os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/rules.yml"
    )

    with open(rules_file, "r") as stream:
        TREE_REWRITE_RULES = yaml.safe_load(stream)
    config = (
        TREE_REWRITE_RULES[args.language]
        if not args.raw and args.language in TREE_REWRITE_RULES
        else EMPTY_CONFIG
    )

    parsers = init_parsers(script_dir)
    doc = parse_and_translate(
        parsers[args.language], config, open(args.file, "rb").read()
    )

    if args.pretty:
        out = StringIO()
        pretty_print_ast(doc.firstChild, out)
        print(out.getvalue())
    else:
        print(doc.toprettyxml())


if __name__ == "__main__":
    main()
