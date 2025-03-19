import sys
from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable


class Assembler:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = input_file.replace(".asm", ".hack")
        self.symbol_table = SymbolTable()

    def assemble(self):
        parser = Parser(self.input_file)
        address = 0

        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType() == "L_COMMAND":
                self.symbol_table.addEntry(parser.symbol(), address)
            else:
                address += 1

        parser = Parser(self.input_file)
        code = Code()
        next_available_address = 16

        with open(self.output_file, "w") as out_file:
            while parser.hasMoreCommands():
                parser.advance()
                if parser.commandType() == "A_COMMAND":
                    symbol = parser.symbol()
                    if symbol.isdigit():
                        address = int(symbol)
                    else:
                        if not self.symbol_table.contains(symbol):
                            self.symbol_table.addEntry(symbol, next_available_address)
                            next_available_address += 1
                        address = self.symbol_table.getAddress(symbol)
                    out_file.write(f"{address:016b}\n")

                elif parser.commandType() == "C_COMMAND":
                    binary_instruction = "111" + code.comp(parser.comp()) + code.dest(parser.dest()) + code.jump(parser.jump())
                    out_file.write(binary_instruction + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    assembler = Assembler(sys.argv[1])
    assembler.assemble()
    print(f"Translation complete. Output written to {assembler.output_file}")
