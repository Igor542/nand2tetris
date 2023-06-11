from Commands import Command, commandType


class Parser:
    def __init__(self, input_filename):
        """Opens the input file and gets ready to parse it."""
        self.input_filename = input_filename
        self.input = open(input_filename, "r")
        self.input_line = None
        self.current_command = None
        pass

    def hasMoreCommands(self):
        """Are there more commands in the input?"""
        self.input_line = self.input.readline()
        while self.input_line and (
            self.input_line[0:2] == "//" or self.input_line.rstrip("\n") == ""
        ):
            self.input_line = self.input.readline()
        if self.input_line:
            self.input_line = self.input_line.rstrip("\n")
            return True
        else:
            return False

    def advance(self):
        """Reads the next command from the input and makes it the current command."""
        self.current_command = self.input_line
        print("[INFO] parser: command: " + self.current_command)

    def commandType(self):
        """Returns a constant representing the type of the current command."""
        c = self.current_command.split(" ")[0]
        return commandType.get(c)

    def arg1(self):
        """Returns the first argument of the current command."""
        words = self.current_command.split(" ")
        if self.commandType() == Command.C_ARITHMETIC:
            return words[0]
        return words[1]

    def arg2(self):
        """Returns the second argument of the current command."""
        return self.current_command.split(" ")[2]

    def currentCommand(self):
        """Returns the command."""
        return self.current_command
