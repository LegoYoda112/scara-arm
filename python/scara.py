import serial
import sys
import time
import re
import threading

class Scara:
    ser = None
    debug = False
    com_port = ""

    def __init__(self, com_port):
        self.com_port = com_port

    def init(self):
        if(self.debug):
            print("Starting scara: " + self.com_port)

        self.ser = serial.Serial(self.com_port, baudrate=115200, timeout = 1)

        if(self.debug):
            print("COM port opened")

    def moveAxisA(self, degrees):
        self.ser.write('')

    def setMoveFeed(self, feedrate):
        command = "M20 F%d" % feedrate
        self.sendCommand(command)

    def debugOn(self):
        self.debug = True

    def debugOff(self):
        self.debug = False

    def sendCommand(self, command):
        if(self.debug):
            print("Sending", command)
        # ser.write(command)
    
    def waitForResponse(self):
        while True:
            if self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8')
                if(debug):
                    print("Received:", line)
                if line == "ok":
                    break