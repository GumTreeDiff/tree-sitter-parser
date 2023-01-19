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
    option(BUILD_SERVER "des1" YES)
    set(SERVER_SRC files_for_test/a.cxx)
    if(APPLE)
        set(APP_VERSION 2)
    else()
        set(APP_VERSION 1)
    endif()

    if(APP_VERSION GREATER 1 OR LINUX)
        list(APPEND SERVER_SRC unix/new.cxx)
    endif()

    add_executable(exec ${SERVER_SRC})
    add_library(lib another_folder_for_test/*.cxx)
    if(foo)
        if(john)
            target_link_libraries(exec lib)
        endif()
    endif()"""

    doc = parse_and_translate(parsers["cmake"], EMPTY_CONFIG, code)
    snapshot.assert_match(doc.toprettyxml(), 'cmake_build.txt')