import sys
import time

import commandObjects
import digital_io_control

run = False  # this controls whether the program runs on hardware
name = "test.txt"
program = {}
reader = open("programs/" + name, "r")

refs = {}  # dictionary which refs are put into

# put the program in a list and \n

for lineNumber, line in enumerate(reader):

    instruction = ""
    code = True  # use to keep track of if the line is a comment
    for character in line:
        if character == "#" or character == "\\"[0]:
            code = False
        if code:
            instruction = instruction + character
    if instruction != "":  # removes lines that are just comments
        # remove any end of line marker
        instruction = instruction.rstrip("\n")
        program[lineNumber] = instruction

# program is in form list of commands
# it is stored in a dictionary so f there is an error the correct line can be returned

# now put it into a dictionary
# list of commands with how much space is needed for them


commands = {}
pos = 0  # position in memory
for line in program:
    instruction = program[line]
    if instruction != "":

        try:
            if "ref" in instruction:  # ref is used to declare a pointer
                if instruction[0:3] != "ref":
                    name = instruction.split(")")[1]  # if name is at the end of a command
                    name = name.strip()
                else:
                    name = instruction  # if ref is on it's own line
                name = name.strip("ref")  # remove ref keyword
                name = name.strip()  # remove spaces
                name = name.rstrip()
                if name == "":  # so no weird un named references get in to the programm
                    # seriously anyone who does this intentionally is a crazy
                    print("error on line ", line)
                    print("you can't declare a reference with no name")
                    print("you won't break my system that easily")
                    sys.exit()
                if name[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    print("error on line ", line)
                    print("names cannot start with a number")
                    sys.exit()
                refs[name] = pos
            if instruction[0:3] != "ref":  # is an instruction not just a reference
                command = instruction.split("(")[0]
                arguments = instruction.split("(")[1].split(")")[0]
                command = commandObjects.getCommand(command, arguments)
                commands[pos] = command
                pos = pos + command.size
                # make new instruction object then check space requirements
                # then allocate it to its position
                # then work out where the next command will go

        except Exception as e:
            print("error on line ", line + 1, "while reading file")
            print(program[line])
            raise e

# currently a dictionary with command start point: object representing that command

# go through and convert to bits
byteCode = {}
for i in commands:
    try:
        commands[i].findNext(refs)
    except Exception as e:
        print("error on line", line, "while getting next lines")
        print(program[line])
        raise e
    byteCode[i] = commands[i].code
    p = 0
    for j in commands[i].next:
        p = p + 1
        byteCode[p + i] = j

out = []  # final code in a list not a dictionary
for i in byteCode:
    out.append(byteCode[i])
print(out)
# this is the part of the program which controls the hardware

if run:
    ioController = digital_io_control.computerController()

    ioController.outputData(out)

    i = 0
    input(">>")
    while True:
        # input(i)
        i += 1
        ioController.pulseClock()
        time.sleep(.2)
