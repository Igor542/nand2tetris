import argparse
import sys

from Commands import Command
from Parser import Parser
from CodeWriter import CodeWriter


def main():
    args = sys.argv
    print(args)
    if len(args) != 2:
        raise Exception("Usage: VMTranslator.py code.vm")

    input_file = args[1]
    output_file = input_file[0:input_file.find(".vm")]+".asm"
    print(input_file + '\n' + output_file)

    p = Parser(input_file)
    cw = CodeWriter(output_file)

    while (p.hasMoreCommands()):
        p.advance()
        ct = p.commandType()
        if ct == Command.C_ARITHMETIC:
            cw.writeArithmetic(p.arg1())
        elif ct == Command.C_PUSH or ct == Command.C_POP:
            cw.writePopPush(ct, p.arg1(), p.arg2())
        else:
            raise Exception("Unknown command type")
    cw.Close()


if __name__ == "__main__":
    main()
