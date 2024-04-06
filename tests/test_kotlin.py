import os
import yaml

from tree_sitter_parser import EMPTY_CONFIG, init_parsers, parse_and_translate


def test_class_definition(snapshot):
    script_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "..")
    rules_file = os.path.join(script_dir, "rules.yml")
    parsers = init_parsers(script_dir)
    with open(rules_file, "r") as stream:
        tree_rewrite_rules = yaml.safe_load(stream)

    with open('./snapshots/test_kotlin/test.kt','r') as ktFile:
        code = ktFile.read()

    doc = parse_and_translate(parsers["kotlin"], tree_rewrite_rules["kotlin"], code.encode('utf-8'))
    snapshot.assert_match(doc.toprettyxml(), 'test_kt_ast.txt')
