#!/usr/bin/env python3

from tree_sitter import Language, Parser
from xml.dom import minidom
from io import StringIO
import os
import argparse
import yaml

script_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
rules_file = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/rules.yml"

EMPTY_CONFIG = {'flattened': [], 'aliased': {}, 'ignored': []}

MAX_LABEL_SIZE = 75

with open(rules_file, "r") as stream:
  TREE_REWRITE_RULES = yaml.safe_load(stream)

Language.build_library(
  script_dir + '/build/languages.so',
  [
    script_dir + '/tree-sitter-c',
    script_dir + '/tree-sitter-c-sharp',
    script_dir + '/tree-sitter-java',
    script_dir + '/tree-sitter-javascript',
    script_dir + '/tree-sitter-ocaml/ocaml',
    script_dir + '/tree-sitter-php',
    script_dir + '/tree-sitter-python',
    script_dir + '/tree-sitter-r',
    script_dir + '/tree-sitter-ruby',
    script_dir + '/tree-sitter-rust',
    script_dir + '/tree-sitter-typescript/typescript'
  ]
)

PARSERS = {
  "c": Language(script_dir + '/build/languages.so', 'c'),
  "csharp": Language(script_dir + '/build/languages.so', 'c_sharp'),
  "java": Language(script_dir + '/build/languages.so', 'java'),
  "javascript": Language(script_dir + '/build/languages.so', 'javascript'),
  "ocaml": Language(script_dir + '/build/languages.so', 'ocaml'),
  "php": Language(script_dir + '/build/languages.so', 'php'),
  "python": Language(script_dir + '/build/languages.so', 'python'),
  "r": Language(script_dir + '/build/languages.so', 'r'),
  "ruby": Language(script_dir + '/build/languages.so', 'ruby'),
  "rust": Language(script_dir + '/build/languages.so', 'rust'),
  "typescript": Language(script_dir + '/build/languages.so', 'typescript'),
}

positions = [0]

doc = minidom.Document()

parser = argparse.ArgumentParser()
parser.add_argument("file", help="path to the file to parse")
parser.add_argument("language", help="language of to the file to parse")
parser.add_argument("--raw", action="store_true", help="deactivate the rewrite rules")
parser.add_argument("--pretty", action="store_true", help="pretty print the AST instead of using XML")
args = parser.parse_args()

def main(file, language):
  parser = Parser()
  parser.set_language(PARSERS[language])
  config = retrieveConfig(language)
  tree = parser.parse(bytes(readFile(file), "utf8"))
  xmlRoot = toXmlNode(tree.root_node, config)
  doc.appendChild(xmlRoot)
  process(tree.root_node, xmlRoot, config)
  if args.pretty:
    out = StringIO()
    pretty_print_ast(doc.firstChild, out)
    print(out.getvalue())
  else:
    print(doc.toprettyxml())

def pretty_print_ast(elm, out, level=0):
  elm_desc = f'\033[1m{elm.getAttribute("type")}\033[0m'
  if elm.hasAttribute("label"):
    elm_desc += f' \033[94m{sanitize_label(elm.getAttribute("label"))}\033[0m'
  left_bound = int(elm.getAttribute("pos"))
  right_bound = left_bound + int(elm.getAttribute("length"))
  elm_desc += f' [{str(left_bound)},{right_bound}]'
  log_start = "" if level == 0 else "\n"
  out.write(f'{log_start}{"  " * level}{elm_desc}')
  for child in elm.childNodes:
    pretty_print_ast(child, out, level + 1)

def sanitize_label(raw_label):
  raw_label = raw_label.replace("\n", "")
  raw_label = raw_label.replace("\t", "")
  label = (raw_label[:MAX_LABEL_SIZE] + '..') if len(raw_label) > MAX_LABEL_SIZE else raw_label
  return label

def process(node, xmlNode, config):
  if not node.type in config['flattened']:
    for child in node.children:
      if not child.type in config['ignored']:
        xmlChildNode = toXmlNode(child, config)
        xmlNode.appendChild(xmlChildNode)
        process(child, xmlChildNode, config)

def retrieveConfig(language):
  return TREE_REWRITE_RULES[language] if not args.raw and language in TREE_REWRITE_RULES else EMPTY_CONFIG

def toXmlNode(node, config):
  xmlNode = doc.createElement('tree')
  type = config['aliased'][node.type] if node.type in config['aliased'] else node.type
  xmlNode.setAttribute("type", type)
  startPos = positions[node.start_point[0]] + node.start_point[1]
  endPos = positions[node.end_point[0]] + node.end_point[1]
  length = endPos - startPos
  xmlNode.setAttribute("pos", str(startPos))
  xmlNode.setAttribute("length", str(length))
  if node.child_count == 0 or node.type in config['flattened']:
    xmlNode.setAttribute("label", node.text.decode('utf8'))
  return xmlNode

def readFile(file):
  with open(file, 'r') as file:
    data = file.read()
  index = 0
  for chr in data:
    index += 1
    if chr == '\n':
      positions.append(index)
  return data

main(args.file, args.language)
