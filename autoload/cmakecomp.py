#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Cmake complete.
"""

import sys
from subprocess import check_output
from pathlib import Path
import json

CMAKE_DICT = {}
CMAKE_DICT_LOADED = False
CMAKE_DICT_FILE = Path(__file__).parent / "cmake_dict.json"


def load_from_file():
    global CMAKE_DICT, CMAKE_DICT_LOADED
    if CMAKE_DICT_FILE.exists():
        try:
            CMAKE_DICT = json.loads(CMAKE_DICT_FILE.read_text("utf-8"))
            CMAKE_DICT_LOADED = True
            return True
        except Exception as e:
            print(str(e), file=sys.stderr)
    return False


def load_dict():
    if CMAKE_DICT_LOADED:
        return
    if not load_from_file():
        print("Cannot load dict file!", file=sys.stderr)


def store_to_file():
    CMAKE_DICT_FILE.write_text(json.dumps(CMAKE_DICT, indent=4), "utf-8")


def expand_name(name):
    if "<CONFIG>" in name:
        yield from expand_name(name.replace("<CONFIG>", "DEBUG"))
        yield from expand_name(name.replace("<CONFIG>", "RELEASE"))
        return
    if "<LANG>" in name:
        yield from expand_name(name.replace("<LANG>", "C"))
        yield from expand_name(name.replace("<LANG>", "CXX"))
        return
    yield name


def vim_escape(s):
    return s.replace("\\", "\\\\").replace('\n', '\\n').replace('"', '\\"')


def extract_subcommand(subcommand):
    ret = check_output(["cmake", f"--help-{subcommand}-list"]).decode("utf-8")
    names = [name.strip() for name in ret.split("\n") if name.strip()]
    for name in names:
        info = check_output(["cmake", f"--help-{subcommand}",
                             name]).decode("utf-8")
        for n in expand_name(name):
            CMAKE_DICT[n] = [vim_escape(info), subcommand]


def gen_dict():
    try:
        for subcommand in ["command", "property", "policy", "variable"]:
            extract_subcommand(subcommand)

        store_to_file()
    except Exception as e:
        print(str(e), file=sys.stderr)


def complete(base):
    import vim
    vim.command("let g:cmakecomp_dict = []")
    load_dict()
    for k, v in CMAKE_DICT.items():
        if k.startswith(base):
            try:
                vim.command(
                    r"""call add(g:cmakecomp_dict, {'word':'%s', 'info':"%s", 'menu':'[%s]', 'icase':0})"""
                    % (k, v[0], v[1]))
            except Exception as e:
                print(str(e), file=sys.stderr)


def main():
    gen_dict()


if __name__ == "__main__":
    main()