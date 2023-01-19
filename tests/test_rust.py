import os

from tree_sitter_parser import EMPTY_CONFIG, init_parsers, parse_and_translate


def test_string_literal_differences():
    script_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "..")
    parsers = init_parsers(script_dir)

    left = b"""
    fn main() {
        let msg = "A";
    }"""

    right = b"""
    fn main() {
        let msg = "B";
    }"""

    config = {"flattened": ["string_literal"], "aliased": {}, "ignored": []}

    got_left = parse_and_translate(parsers["rust"], config, left)
    got_right = parse_and_translate(parsers["rust"], config, right)

    assert got_left != got_right, "Trees should have been different."
