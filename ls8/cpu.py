"""CPU functionality."""

import sys
import math

############################################################

BIT__COUNT = 8
BIT__MASK = int(bin((2 ** BIT__COUNT) - 1), base=2)

HEX__COUNT = math.ceil(BIT__COUNT / 4)
FORMAT = f"0x%0{HEX__COUNT}X"

# OCT__COUNT = math.ceil(BIT__COUNT / 3)
# FORMAT = f"0o%0{OCT__COUNT}o"

#-----------------------------------------------------------


def mask(value, binary_mask=BIT__MASK):
    """Mask the provided `value` to clip it to the required number of bits."""

    return (value & binary_mask)


############################################################
#   "Binary" helper classes
############################################################


class BinaryItem:
    """A class to manage binary items."""

    def __init__(self, value):

        self.value = value
        return

    def __str__(self):

        # return (f"0o%0{OCT__COUNT}o" % self.value)
        return (FORMAT % self.value)

    @property
    def value(self):

        return self.__value

    @value.setter
    def value(self, value):

        self.__value = mask(value)
        return


class BinaryItemSequence:
    """A class to manage sequences of binary items."""

    def __init__(self, sequence):

        self.sequence = sequence
        return

    def __str__(self):

        return ("[" + ", ".join(str(item) for item in self.sequence) + "]")

    def __len__(self):

        return len(self.sequence)

    def __getitem__(self, key):

        return self.sequence[key]

    def __setitem__(self, key, value):

        self.sequence[key].value = value
        return

    @property
    def sequence(self):

        return self.__sequence

    @sequence.setter
    def sequence(self, sequence):

        self.__sequence = [BinaryItem(value) for value in sequence]
        return


############################################################
#   CPU
############################################################


class CPU:
    """Main CPU class."""

    ############################################################

    def __init__(self):
        """Construct a new CPU."""

        self.memory = [0] * BIT__COUNT

        self.program = []
        self.program_pointer = 0

        self.stack = []
        self.stack_pointer = 0

        self.flags = 0

        return

    ############################################################

    def read_memory(self, address):
        """Read the `value` from the provided `address` in memory."""

        return self.memory[address]

    def write_memory(self, address, value):
        """Write the `value` to the provided `address` in memory."""

        self.memory[address] = mask(value)

        return

    ############################################################

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.write_memory(address, instruction)
            address += 1

    ############################################################

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            value_a = self.read_memory(reg_a)
            value_b = self.read_memory(reg_b)
            self.write_memory(reg_a, value_a + value_b)
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    ############################################################

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE --- {FORMAT} {FORMAT} {FORMAT} | {FORMAT} {FORMAT} {FORMAT} |" % (
                self.program_pointer,
                self.stack_pointer,
                self.flags,
                self.read_memory(self.pc),
                self.read_memory(self.pc + 1),
                self.read_memory(self.pc + 2),
            ),
            end="",
        )

        for address in range(BIT__COUNT):
            print(f" {FORMAT}" % self.read_memory(address), end="")

        print()

    ############################################################

    def run(self):
        """Run the CPU."""
        pass
