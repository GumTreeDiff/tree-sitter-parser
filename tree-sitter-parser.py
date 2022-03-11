#!/usr/bin/env python3

from tree_sitter import Language, Parser
from xml.dom import minidom
import sys
import os

script_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

TREE_REWRITE_RULES = {
  'java': { 
    'flattened': ['scoped_identifier', 'integral_type', 'array_type', 'generic_type', 'scoped_type_identifier'], 
    'aliased': {'+=': 'affectation_operator', '-=': 'affectation_operator', '*=': 'affectation_operator', '/=': 'affectation_operator', '=': 'affectation_operator', '|=': 'affectation_operator', '&=': 'affectation_operator', '^=': 'affectation_operator', '-': 'arithmetic_operator', '+': 'arithmetic_operator', '/': 'arithmetic_operator', '*': 'arithmetic_operator', '==': 'comparison_operator', '<': 'comparison_operator', '<=': 'comparison_operator', '>': 'comparison_operator', '>=': 'comparison_operator', '!=': 'comparison_operator', '&&': 'logical_operator', '||': 'logical_operator', '++': 'increment_operator', '--': 'increment_operator', '&': 'bitwise_operator', '|': 'bitwise_operator', '^': 'bitwise_operator', 'scoped_identifier': 'identifier', 'public': 'visibility', 'protected': 'visibility', 'private': 'visibility', 'class_declaration': 'type_declaration', 'interface_declaration': 'type_declaration', 'enum_declaration': 'type_declaration', 'integral_type': 'type', 'type_identifier': 'type', 'array_type': 'type', 'generic_type': 'type', 'scoped_type_identifier': 'type', 'enhanced_for_statement': 'for_statement', 'class': 'type_keyword', 'interface': 'type_keyword', 'enum': 'type_keyword', 'class_body': 'type_body', 'interface_body': 'type_body', 'enum_body': 'type_body'}, 
    'ignored': [';', '{', '}', '(', ')', '[', ']', '.', 'import', 'return', 'for']},
}

Language.build_library(
  script_dir + '/build/languages.so',
  [
    script_dir + '/tree-sitter-c',
    script_dir + '/tree-sitter-java',
    script_dir + '/tree-sitter-javascript',
    script_dir + '/tree-sitter-r',
    script_dir + '/tree-sitter-ocaml/ocaml',
    script_dir + '/tree-sitter-php',
    script_dir + '/tree-sitter-python',
    script_dir + '/tree-sitter-ruby',
    script_dir + '/tree-sitter-typescript/typescript'
  ]
)

PARSERS = {
  "c": Language(script_dir + '/build/languages.so', 'c'),
  "java": Language(script_dir + '/build/languages.so', 'java'),
  "javascript": Language(script_dir + '/build/languages.so', 'javascript'),
  "ocaml": Language(script_dir + '/build/languages.so', 'ocaml'),
  "php": Language(script_dir + '/build/languages.so', 'php'),
  "python": Language(script_dir + '/build/languages.so', 'python'),
  "r": Language(script_dir + '/build/languages.so', 'r'),
  "ruby": Language(script_dir + '/build/languages.so', 'ruby'),
  "typescript": Language(script_dir + '/build/languages.so', 'typescript'),
}

positions = [0]

doc = minidom.Document()

def main(file, language):
  parser = Parser()
  parser.set_language(PARSERS[language])
  config = retrieveConfig(language)
  tree = parser.parse(bytes(readFile(file), "utf8"))
  xmlRoot = toXmlNode(tree.root_node, config)
  doc.appendChild(xmlRoot)
  process(tree.root_node, xmlRoot, config)
  xml = doc.toprettyxml()
  print(xml)

def process(node, xmlNode, config):
  if not node.type in config['flattened']:
    for child in node.children:
      if not child.type in config['ignored']:
        xmlChildNode = toXmlNode(child, config)
        xmlNode.appendChild(xmlChildNode)
        process(child, xmlChildNode, config)

def retrieveConfig(language):
  return TREE_REWRITE_RULES[language] if language in TREE_REWRITE_RULES else { 'flattened': [], 'aliased': {}, 'ignored': []}

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

if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])