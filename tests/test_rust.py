import os
import yaml

from tree_sitter_parser import EMPTY_CONFIG, init_parsers, parse_and_translate


def test_string_literal_differences():
    script_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "..")
    rules_file = os.path.join(script_dir, "rules.yml")
    parsers = init_parsers(script_dir)
    with open(rules_file, "r") as stream:
        tree_rewrite_rules = yaml.safe_load(stream)

    left = b"""
    fn main() {
        let msg = "A";
    }"""

    right = b"""
    fn main() {
        let msg = "B";
    }"""

    got_left = parse_and_translate(parsers["rust"], tree_rewrite_rules["rust"], left)
    got_right = parse_and_translate(parsers["rust"], tree_rewrite_rules["rust"], right)

    assert got_left != got_right, "Trees should have been different."
