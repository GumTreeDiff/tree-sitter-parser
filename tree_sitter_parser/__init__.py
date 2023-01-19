import sys
from xml.dom import minidom

from tree_sitter import Language, Parser


EMPTY_CONFIG = {"flattened": [], "aliased": {}, "ignored": []}
MAX_LABEL_SIZE = 75


def eprint(*args, **kwargs):
    """
    Same as `print` but writes to `sys.stderr`.
    """
    print(*args, file=sys.stderr, **kwargs)


def init_parsers(script_dir):
    """
    Compile parsers (when needed) and return a parser map that can be indexed by language.
    """
    if Language.build_library(
        script_dir + "/build/languages.so",
        [
            script_dir + "/tree-sitter-c",
            script_dir + "/tree-sitter-c-sharp",
            script_dir + "/tree-sitter-cmake",
            script_dir + "/tree-sitter-java",
            script_dir + "/tree-sitter-javascript",
            script_dir + "/tree-sitter-ocaml/ocaml",
            script_dir + "/tree-sitter-php",
            script_dir + "/tree-sitter-python",
            script_dir + "/tree-sitter-r",
            script_dir + "/tree-sitter-ruby",
            script_dir + "/tree-sitter-rust",
            script_dir + "/tree-sitter-typescript/typescript",
        ],
    ):
        eprint("Compiled dynamic library of parsers.")
    else:
        eprint("Reusing dynamic library of parsers.")

    return {
        "c": Language(script_dir + "/build/languages.so", "c"),
        "csharp": Language(script_dir + "/build/languages.so", "c_sharp"),
        "cmake": Language(script_dir + "/build/languages.so", "cmake"),
        "java": Language(script_dir + "/build/languages.so", "java"),
        "javascript": Language(script_dir + "/build/languages.so", "javascript"),
        "ocaml": Language(script_dir + "/build/languages.so", "ocaml"),
        "php": Language(script_dir + "/build/languages.so", "php"),
        "python": Language(script_dir + "/build/languages.so", "python"),
        "r": Language(script_dir + "/build/languages.so", "r"),
        "ruby": Language(script_dir + "/build/languages.so", "ruby"),
        "rust": Language(script_dir + "/build/languages.so", "rust"),
        "typescript": Language(script_dir + "/build/languages.so", "typescript"),
    }


def parse_and_translate(parser_lang, config, input: bytes):
    """
    Parse a file and translate the obtained AST to the GumTree XML format.
    """
    newline_offsets = create_newline_offsets(input)

    parser = Parser()
    parser.set_language(parser_lang)
    tree = parser.parse(input)

    doc = minidom.Document()
    xml_root = to_xml_node(doc, tree.root_node, config, newline_offsets)
    doc.appendChild(xml_root)
    process(doc, tree.root_node, xml_root, config, newline_offsets)

    return doc


def create_newline_offsets(input: bytes):
    """
    Obtain a list of indices of all newlines in a file. The first line has offset 0.

    This list can be used to translate from `(line, column)` to `pos` by using ...

        pos = offsets[line] + column
    """
    offsets = [0]

    for (i, chr) in enumerate(input.decode("utf-8"), start=1):
        if chr == "\n":
            offsets.append(i)

    return offsets


def process(doc, node, xml_node, config, newline_offsets):
    """
    Process a given node of the ast to include it in a given xml document.
    """
    if not node.type in config["flattened"]:
        for child in node.children:
            if not child.type in config["ignored"]:
                xml_child_node = to_xml_node(doc, child, config, newline_offsets)
                xml_node.appendChild(xml_child_node)
                process(doc, child, xml_child_node, config, newline_offsets)


def to_xml_node(doc, node, config, newline_offsets):
    """
    Converts an AST node into a XML node.
    """
    xmlNode = doc.createElement("tree")
    type = config["aliased"][node.type] if node.type in config["aliased"] else node.type
    xmlNode.setAttribute("type", type)
    startPos = newline_offsets[node.start_point[0]] + node.start_point[1]
    endPos = newline_offsets[node.end_point[0]] + node.end_point[1]
    length = endPos - startPos
    xmlNode.setAttribute("pos", str(startPos))
    xmlNode.setAttribute("length", str(length))
    if node.child_count == 0 or node.type in config["flattened"]:
        xmlNode.setAttribute("label", node.text.decode("utf8"))
    return xmlNode


def pretty_print_ast(elm, out, level=0):
    """
    Outputs the AST into a human-readable format.
    """
    elm_desc = f'\033[1m{elm.getAttribute("type")}\033[0m'
    if elm.hasAttribute("label"):
        elm_desc += f' \033[94m{sanitize_label(elm.getAttribute("label"))}\033[0m'
    left_bound = int(elm.getAttribute("pos"))
    right_bound = left_bound + int(elm.getAttribute("length"))
    elm_desc += f" [{str(left_bound)},{right_bound}]"
    log_start = "" if level == 0 else "\n"
    out.write(f'{log_start}{"  " * level}{elm_desc}')
    for child in elm.childNodes:
        pretty_print_ast(child, out, level + 1)


def sanitize_label(raw_label):
    raw_label = raw_label.replace("\n", "")
    raw_label = raw_label.replace("\t", "")
    label = (
        (raw_label[:MAX_LABEL_SIZE] + "..")
        if len(raw_label) > MAX_LABEL_SIZE
        else raw_label
    )
    return label
