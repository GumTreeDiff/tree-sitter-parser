#!/usr/bin/env python3

from tree_sitter import Language, Parser
from xml.dom import minidom
import sys
import os

script_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

Language.build_library(
  script_dir + '/build/languages.so',
  [
    script_dir + '/tree-sitter-c',
    script_dir + '/tree-sitter-python',
    script_dir + '/tree-sitter-java',
    script_dir + '/tree-sitter-javascript',
    script_dir + '/tree-sitter-r',
    script_dir + '/tree-sitter-ocaml/ocaml',
    script_dir + '/tree-sitter-typescript/typescript'
  ]
)

PARSERS = {
  "c": Language(script_dir + '/build/languages.so', 'c'),
  "java": Language(script_dir + '/build/languages.so', 'java'),
  "javascript": Language(script_dir + '/build/languages.so', 'javascript'),
  "ocaml": Language(script_dir + '/build/languages.so', 'ocaml'),
  "python": Language(script_dir + '/build/languages.so', 'python'),
  "r": Language(script_dir + '/build/languages.so', 'java'),
  "typescript": Language(script_dir + '/build/languages.so', 'typescript'),
}

positions = [0]

doc = minidom.Document()

def main(file, language):
  parser = Parser()
  parser.set_language(PARSERS[language])
  tree = parser.parse(bytes(readFile(file), "utf8"))
  xmlRoot = toXmlNode(tree.root_node)
  doc.appendChild(xmlRoot)
  process(tree.root_node, xmlRoot)
  xml = doc.toprettyxml()
  print(xml)

def process(node, xmlNode):
  for child in node.children:
    xmlChildNode = toXmlNode(child)
    xmlNode.appendChild(xmlChildNode)
    process(child, xmlChildNode)

def toXmlNode(node):
  xmlNode = doc.createElement('tree')
  xmlNode.setAttribute("type", node.type)
  startPos = positions[node.start_point[0]] + node.start_point[1]
  endPos = positions[node.end_point[0]] + node.end_point[1]
  length = endPos - startPos
  xmlNode.setAttribute("pos", str(startPos))
  xmlNode.setAttribute("length", str(length))
  if node.child_count == 0:
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