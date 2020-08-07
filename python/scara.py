import serial
import sys
import time
import re
import threading

class Scara:
    ser = None
    debug = False
    com_port = ""

    A_deg = 0
    B_deg = 0
    C_deg = 0
    D_deg = 0

    def __init__(self, com_port):
        self.com_port = com_port

    def init(self):
        if(self.debug):
            print("Starting scara: " + self.com_port)

        self.ser = serial.Serial(self.com_port, baudrate=9600, timeout = 1)
        self.waitForResponse()

        if(self.debug):
            print("COM port opened")

    def moveAxisATo(self, degrees):
        self.A_deg = degrees
        command = "M20 A%d" % degrees
        self.sendCommand(command)
    
    def moveAxisBTo(self, degrees):
        self.B_deg = degrees
        command = "M20 A%d" % degrees
        self.sendCommand(command)

    def moveAxisABTo(self, A_degrees, B_degrees):
        self.A_deg = A_degrees
        self.B_deg = B_degrees
        command = "M20 A%d B%d" % (A_degrees, B_degrees)
        self.sendCommand(command)

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
        command += "\n"
        self.ser.write(command.encode())
        self.waitForResponse()
    
    # Wait for "ok" response
    def waitForResponse(self):
        if self.debug:
            print("Waiting for response")
        while True:
            if self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8')[:-2]
                if(self.debug):
                    print("-", line)
                if line == "ok":
                    break