from pathlib import Path

import Commands
from Commands import Command


class CodeWriter:
    def __init__(self, output_filename):
        """Opens the output file and gets ready to write into it."""
        self.output_filename = output_filename
        self.output = open(output_filename, "w")

    def setFileName(self, input_file):
        """Informs the codeWriter that the translation of a new VM file
        has started.
        """
        self.current_file = input_file

    def writeArithmetic(self, command):
        """Writes to the output file the assembly code that implements
        the given arithmetic command.
        """
        print("[INFO] codewriter: " + command)
        asm = Commands.commandAsm.get(command)
        gen = asm()
        self.output.write("\n".join(gen) + "\n")

    def writeInit(self):
        """Writes the assembly instructions that effect the bootstrap code
        that initializes the VM. Should be placed at the beginning of
        the generated .asm file.
        """
        asm = Commands.commandAsm.get("startup")
        gen = asm()
        self.output.write("\n".join(gen) + "\n")

    def writeLabel(self, label):
        """Writes assembly code that effects the label command."""
        print("[INFO] codewriter: " + label)
        asm = Commands.commandAsm.get("label")
        gen = asm(label)
        self.output.write("\n".join(gen) + "\n")

    def writeGoto(self, label):
        """Writes assembly code that effects the goto command."""
        print("[INFO] codewriter: " + label)
        asm = Commands.commandAsm.get("goto")
        gen = asm(label)
        self.output.write("\n".join(gen) + "\n")

    def writeIf(self, label):
        """Writes assembly code that effects the if command."""
        print("[INFO] codewriter: " + label)
        asm = Commands.commandAsm.get("if")
        gen = asm(label)
        self.output.write("\n".join(gen) + "\n")

    def writeFunction(self, name, nargs):
        """Writes assembly code that effects the function command."""
        print("[INFO] codewriter: " + name + " " + nargs)
        asm = Commands.commandAsm.get("function")
        gen = asm(name, nargs)
        self.output.write("\n".join(gen) + "\n")

    def writeCall(self, name, nargs):
        """Writes assembly code that effects the call command."""
        print("[INFO] codewriter: " + name + " " + nargs)
        asm = Commands.commandAsm.get("call")
        gen = asm(name, nargs)
        self.output.write("\n".join(gen) + "\n")

    def writeReturn(self):
        """Writes assembly code that effects the return command."""
        print("[INFO] codewriter: return")
        asm = Commands.commandAsm.get("return")
        gen = asm()
        self.output.write("\n".join(gen) + "\n")

    def writePopPush(self, command, segment, index):
        """Writes to the output file the assembly code that implements
        the given command, where command is either C_PUSH or C_POP.
        """
        command_str = "push" if command == Command.C_PUSH else "pop"
        asm = Commands.commandAsm.get(command_str)
        print("[INFO] codewriter: " + command_str + " " + segment)
        gen = asm(segment, index)
        self.output.write("\n".join(gen) + "\n")

    def writeComment(self, comment):
        self.output.write(f"// {comment}\n")

    def Close(self):
        """Closes the output file."""
        self.output.close()
