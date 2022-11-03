import commandObjects


def bintest1():
    x = commandObjects.toBinary(107, 8)
    if x == "01101011":
        print("bintest1 passed")
    else:
        print("bintest1 failed", x)


def bintest2():
    x = commandObjects.toBinary(107, 16)
    if x == "0000000001101011":
        print("bintest2 passed")
    else:
        print("bintest2 failed", x)


def negBintest1():
    x = commandObjects.toBinary(-2, 3)
    if x == "111":
        print("negBintest1 passed")
    else:
        print("negBintest1 failed", x)


def createConstantTest1():
    x = commandObjects.getCommand("dec", "107")
    if x.code == "01101011":
        print("createConstantTest1 passed")
    else:
        print("createConstantTest1 failed")


def createConstantTest2():
    x = commandObjects.getCommand("bin", "10")
    if x.code == "00000010":
        print("createConstantTest2 passed")
    else:
        print("createConstantTest2 failed", x.code)


def createLongConstantTest1():
    x = commandObjects.getCommand("longBin", "2,111111111")
    if x.code == "00000001" and x.next[0] == "11111111":
        print("createLongConstantTest1 passed")
    else:
        print("createLongConstantTest1 failed", x.code, x.next)


def createDecLongConstantTest1():
    x = commandObjects.getCommand("longDec", "2,33247")
    if x.code == "10000001" and x.next[0] == "11011111":
        print("createDecLongConstantTest1 passed")
    else:
        print("createDecLongConstantTest1 failed", x.code, x.next)


def createAddTest():
    x = commandObjects.getCommand("add", "cake")
    if x.code == "01110100":
        print("createAddTest passed")
    else:
        print("createAddTest failed")


def readAddTest():
    x = commandObjects.getCommand("add", "cake")
    x.findNext({"cake": 107})
    if x.next[1] == "01101011" and x.next[0] == "00000000":
        print("readeAddTest passed")
    else:
        print("readAddTest failed", x.next)


def readAddTest2():
    x = commandObjects.getCommand("add", "cake[1]")
    x.findNext({"cake": 107})
    if x.next[1] == "01101100" and x.next[0] == "00000000":
        print("readeAddTest2 passed")
    else:
        print("readAddTest2 failed", x.next)


def constantToLargeTest():
    try:
        x = commandObjects.getCommand("dec", "1070")
        print("constantToLargeTest failed")
    except:
        print("constantToLargeTest passed")


def isBinaryTest1():
    if commandObjects.isBinary("101010101010101001010101010101001"):
        print("isBinaryTest1 passed")
    else:
        print("isBinaryTest1 failed")


def isBinaryTest2():
    if commandObjects.isBinary("1010106101010101001010101010101001"):
        print("isBinaryTest2 failed")
    else:
        print("isBinaryTest2 passed")


bintest1()
bintest2()
negBintest1()
createConstantTest1()
createConstantTest2()
createLongConstantTest1()
createDecLongConstantTest1()
createAddTest()
readAddTest()
readAddTest2()
constantToLargeTest()
isBinaryTest1()
isBinaryTest2()
