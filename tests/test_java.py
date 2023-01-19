import os

import yaml

from tree_sitter_parser import EMPTY_CONFIG, init_parsers, parse_and_translate


def test_class_definition(snapshot):
    script_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "..")
    rules_file = os.path.join(script_dir, "rules.yml")
    parsers = init_parsers(script_dir)
    with open(rules_file, "r") as stream:
        tree_rewrite_rules = yaml.safe_load(stream)

    code = b"""
    public class Foo<E> extends Bar {
        String bar = new String();

        private void foo() {
            return null;
        }     
    }"""

    doc = parse_and_translate(parsers["java"], tree_rewrite_rules["java"], code)
    snapshot.assert_match(doc.toprettyxml(), 'java_ast_classdef.txt')