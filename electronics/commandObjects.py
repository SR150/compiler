import math


class unknownArguments(Exception):
    pass


class unknownInstruction(Exception):
    pass


class inputToBig(Exception):
    pass


def isBinary(n):
    for c in n:
        if c != "1" and c != "0":
            return False
    return True


def negToBinary(n, length):  # returns 2s complement form of a negative number
    n = abs(n)
    if n > 2 ** length:
        raise inputToBig()
    binary = toBinary(n, length)
    # flip bits
    flipped = ""
    for digit in binary:
        if digit == "1":
            flipped += "0"
        else:
            flipped += "1"

    # add one
    out = ""
    done = False
    for digit in flipped:
        if done:
            out += digit
        else:
            if digit == "0":
                done = True
            out += "1"
    return out


def toBinary(n, length):  # converts int n to a optionally signed binary string of length length
    o = ""
    if n < 0:
        return negToBinary(n, length)
    if n >= 2 ** (length + 1):
        raise inputToBig()
    for i in range(length):
        if n >= (2 ** (length - i - 1)):
            n = n - 2 ** (length - i - 1)
            o = o + "1"
        else:
            o = o + "0"
    return o


def getCommand(instruction, arguments):
    commands = {"resetAcc": lambda x: resetAcc(x),
                "bin": lambda x: binaryConstant(x),
                "dec": lambda x: decimalConstant(x),
                "add": lambda x: add(x),
                "minus": lambda x: minus(x),
                "halt": lambda x: stopClock(x),
                "jump": lambda x: jump(x),
                "longBin": lambda x: longConstant(x),
                "longDec": lambda x: longDecConstant(x)}

    if instruction in commands:
        arguments = arguments.split(",")
        command = commands[instruction](arguments)
        return command
    else:
        raise unknownInstruction("unrecognized command", instruction)


class commandInner:
    size = 0  # number of bytes taken up
    code = ""
    args = []
    next = []  # holds any extra data such as adresses

    def __init__(self, arguments):
        self.args = arguments
        self.next = []

    def findNext(self, refs):
        pass  # finds the next bytes for multi item things
        # needs to be done at the end so references have all been found


class resetAcc(commandInner):
    size = 1
    code = "00110000"


class pauseClock(commandInner):
    size = 1
    code = "01110010"


class addressInstruction(commandInner):  # this is a parent to any command that is a command then an address
    size = 3
    code = ""

    def __init__(self, arguments):
        if len(arguments) != 1:
            raise unknownArguments("expected 1 argument (an address) got ", len(arguments))
        self.args = arguments

    def findAddress(self, refs, arg):
        offset = 0
        if "[" in arg:
            temp = arg.split("[")
            arg = temp[0]
            try:
                offset = temp[1]
                offset = offset.rstrip("]")
                offset = int(offset)
            except:
                raise unknownArguments("not a valid number or reference name")
        if arg in refs:
            arg = refs[arg] + offset
        try:
            arg = toBinary(int(arg), 16)
        except:
            raise unknownArguments("not a valid number or reference name")
        return [arg[0:8], arg[8:]]

    def findNext(self, refs):
        self.next = self.findAddress(refs, self.args[0])


class add(addressInstruction):
    code = "01110100"


class minus(addressInstruction):
    code = "01110101"


class branch(addressInstruction):
    code = "01110110"


class binaryConstant(commandInner):
    size = 1

    def __init__(self, arguments):
        if len(arguments) != 1:
            raise unknownArguments("unknown argument combination")
        self.args = arguments[0]
        if len(self.args) > 8:
            raise unknownArguments("unknown argument maybe it is too long check it is only 8 digits")
        if not isBinary(self.args):
            raise unknownArguments("That argument is not in binary make sure it contains only 1s and 0s")
        # fill in start with 0s to make to 8
        self.code = "0" * (8 - len(self.args)) + self.args


class decimalConstant(binaryConstant):

    def __init__(self, arguments):
        if len(arguments) != 1:
            raise unknownArgument("unknown argument combination")
        self.args = arguments[0]

        try:
            self.args = int(self.args)
        except:
            raise unknownArgument("that value isn't a number")

        if self.args > 127 or self.args < -128:
            raise unknownArgument("that value is too big to be a 8 bit signed number")
        self.code = toBinary(self.args, 8)


class longConstant(commandInner):
    def __init__(self, arguments):
        if len(arguments) != 2:
            raise unknownArgument("unknown argument combination")
        try:
            self.size = int(arguments[0])
            value = arguments[1]
        except:
            raise unknownArgument("unknown argument combination check they are both integers")

        if not isBinary(self.args):
            raise unknownArguments("That argument is not in binary make sure it contains only 1s and 0s")

        if len(value) >= (self.size * 8 + 1):
            raise unknownArgument("that value is too big to go in the number you have specified. "
                                  "please remember the arguments are size(in bytes),value")

        # add 0s to make the value to the required length
        value = "0" * (self.size * 8 - len(value)) + value

        # convert to list in next
        self.code = value[0:8]
        self.next = []
        for i in range(self.size - 1):
            self.next.append(value[(i + 1) * 8:(i + 2) * 8])


class longDecConstant(longConstant):
    def __init__(self, arguments):
        if len(arguments) != 2:
            raise unknownArgument("unknown argument combination")
        try:
            value = int(arguments[1])
        except:
            raise unknownArgument("unknown argument combination check they are both integers")
        value = toBinary(value, int(math.log2(value) + 3))
        value = value.lstrip("0")
        longConstant.__init__(self, [arguments[0], value])
