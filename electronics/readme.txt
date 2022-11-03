This is a basic compiler for a computer I am building. It takes a txt file  reads it and outputs the instructions that can be loaded directly onto the computer.

It can handle variables. variables are expressed as pointers.
Not all operations are implemented but it is set up to be easy to implement new ones. For example the code for add is
class add(addressInstruction):
    code = "01110100"
and an extra entry in a dictionary in the get command method. Most instructions can be created with that little code though some will require more mainly
around error checking.
