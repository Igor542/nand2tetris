import argparse
import sys
import os

import Commands
from Commands import Command
from Parser import Parser
from CodeWriter import CodeWriter
from pathlib import Path


def vm_sources(path):
    sources = []
    if os.path.isdir(path):
        for file in os.listdir(path):
            filename = os.path.join(path, file)
            if os.path.isfile(filename) and filename.find(".vm") != -1:
                sources.append(filename)
    else:
        if path.find(".vm") != -1:
            sources.append(path)
        else:
            raise Exception("input file is not a .vm")

    print(sources)
    return sources


def translate(input_file, cw):
    p = Parser(input_file)
    Commands.filename = Path(input_file).stem

    while p.hasMoreCommands():
        p.advance()
        cw.writeComment(p.currentCommand())
        ct = p.commandType()
        if ct == Command.C_ARITHMETIC:
            cw.writeArithmetic(p.arg1())
        elif ct == Command.C_PUSH or ct == Command.C_POP:
            cw.writePopPush(ct, p.arg1(), p.arg2())
        elif ct == Command.C_LABEL:
            cw.writeLabel(p.arg1())
        elif ct == Command.C_IF:
            cw.writeIf(p.arg1())
        elif ct == Command.C_GOTO:
            cw.writeGoto(p.arg1())
        elif ct == Command.C_FUNCTION:
            cw.writeFunction(p.arg1(), p.arg2())
        elif ct == Command.C_CALL:
            cw.writeCall(p.arg1(), p.arg2())
        elif ct == Command.C_RETURN:
            cw.writeReturn()
        else:
            cmd = p.currentCommand()
            raise Exception(f"Unknown command: {cmd}")


def main():
    args = sys.argv
    print(args)
    if len(args) != 2:
        raise Exception("Usage: VMTranslator.py code.vm")

    input_file = args[1]
    is_dir = False
    if os.path.isdir(input_file):
        is_dir = True
        dir_file = os.path.abspath(input_file)
        output_file = dir_file + "/" + os.path.basename(dir_file) + ".asm"
    else:
        output_file = input_file[0 : input_file.find(".vm")] + ".asm"

    print("Output file: " + output_file)
    cw = CodeWriter(output_file)
    if is_dir:
        cw.writeInit()

    for s in vm_sources(input_file):
        translate(s, cw)

    cw.Close()


if __name__ == "__main__":
    main()
