import serial as serial
import time
import controller
#0-3 data out
#4 clock for out shift register
#5 reset counter
#6 clock
#7 read write
class computerController(controller.DigitalIoController):
    state = [0, 0, 0, 0, 0, 0, 0, 0]
    t=0.05
    def __init__(self):
        self.ser = serial.Serial('COM3', 9600)

    def set(self, newState):  # set a new output
        if len(newState) == 8 and isinstance(newState, list) and isinstance(newState[0], int):
            self.state = newState
            self.update()
        else:
            raise Exception("unknown argument maybe it is too long check it is only 8 digits")

    def setBit(self, index, value):
        if value == 0 or value == 1:
            self.state[index] = value
            self.update()

    def update(self):  # put output on chip
        value = 0  # convert list of outputs to value to put on chip
        for i in range(8):
            value = value + self.state[i] * 2 ** i
        self.putDataAsync(value)
    def pulseClock(self):
        self.setBit(6, 1)
        time.sleep(self.t)
        self.setBit(6, 0)

    def resetCounter(self):
        self.setBit(5,0)
        time.sleep(self.t)
        self.pulseClock()
        time.sleep(self.t)
        self.setBit(5,1)

    def outputData(self, data):

        out = []
        for byte in data:
            # sends first 2 digits to latches then sends the first 6
            #come in most significant bit first
            #then conver to least significant bit first
            if len(byte)!=8:
                raise Exception("byte is not 8 bits long ",byte)
            pair = [[int(byte[4]), int(byte[5]), int(byte[6]), int(byte[7]), 0, 1, 0, 1],[int(byte[0]), int(byte[1]), int(byte[2]), int(byte[3]), 0, 1, 0,1]]

            out.append(pair)

        self.resetCounter()
        i=0
        for pair in out:
            time.sleep(self.t)
            self.set(pair[0])  # set first 4 digits

            time.sleep(self.t)  # send to d type latches
            self.setBit(4, 1)
            time.sleep(self.t)
            self.setBit(4, 0)
            # set next 4 bits
            self.set(pair[1])
            time.sleep(self.t)
            #print(pair)
            #input(i)
            i+=1

            self.pulseClock()

        time.sleep(self.t)
        self.setBit(7,0)
        time.sleep(self.t)
        self.resetCounter()

if __name__ == "__main__":
    ioController = computerController()
    #ioController.putDataAsync(3)
    ioController.outputData(['00111001','00000000'])
