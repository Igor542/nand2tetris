from pathlib import Path

import Commands
from Commands import Command


class CodeWriter:
    def __init__(self, output_filename):
        """ Opens the output file and gets ready to write into it.
        """
        self.output_filename = output_filename
        self.output = open(output_filename, 'w')
        Commands.filename = Path(output_filename).stem

    def writeArithmetic(self, command):
        """ Writes to the output file the assembly code that implements
            the given arithmetic command.
        """
        print("[INFO] codewriter: " + command)
        asm = Commands.commandAsm.get(command)
        gen = asm()
        self.output.write('\n'.join(gen) + '\n')

    def writePopPush(self, command, segment, index):
        """ Writes to the output file the assembly code that implements
            the given command, where command is either C_PUSH or C_POP.
        """
        command_str = 'push' if command == Command.C_PUSH else 'pop'
        asm = Commands.commandAsm.get(command_str)
        print("[INFO] codewriter: " + command_str + ' ' + segment)
        gen = asm(segment, index)
        self.output.write('\n'.join(gen) + '\n')

    def Close(self):
        """ Closes the output file.
        """
        self.output.close()
