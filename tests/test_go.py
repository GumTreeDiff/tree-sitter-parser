import os

import yaml

from tree_sitter_parser import EMPTY_CONFIG, init_parsers, parse_and_translate


def test_go(snapshot):
    script_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "..")
    rules_file = os.path.join(script_dir, "rules.yml")
    parsers = init_parsers(script_dir)
    with open(rules_file, "r") as stream:
        tree_rewrite_rules = yaml.safe_load(stream)

    code = b"""
    package main
    import "fmt"
    func main() {
        fmt.Println("hello world")
    }"""

    doc = parse_and_translate(parsers["go"], tree_rewrite_rules["go"], code)
    snapshot.assert_match(doc.toprettyxml(), 'go_hello_world.txt')