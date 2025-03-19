import re

class Parser:
    def __init__(self, input_file):
        with open(input_file, "r") as file:
            self.lines = [line.strip() for line in file.readlines() if line.strip() and not line.startswith("//")]
        self.current_command = None
        self.current_index = -1

    def hasMoreCommands(self):
        return self.current_index + 1 < len(self.lines)

    def advance(self):
        self.current_index += 1
        self.current_command = self.lines[self.current_index].split("//")[0].strip()
    def commandType(self):
        if self.current_command.startswith("@"):
            return "A_COMMAND"
        elif self.current_command.startswith("(") and self.current_command.endswith(")"):
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self):
        if self.commandType() == "A_COMMAND":
            return self.current_command[1:]
        elif self.commandType() == "L_COMMAND":
            return self.current_command[1:-1]

    def dest(self):
        return self.current_command.split('=')[0] if "=" in self.current_command else ""

    def comp(self):
        parts = self.current_command.split("=")
        remainder = parts[1] if len(parts) > 1 else parts[0]
        return remainder.split(";")[0]

    def jump(self):
        return self.current_command.split(";")[1] if ";" in self.current_command else ""
