import serial
import time
import re
import math

import ik

class Scara:
    # TODO: Figure out how to make these not able to be changed outside the class
    ser = None
    debug = False
    com_port = ""

    # Stores current (blind) axis rotation
    A_deg = 0
    B_deg = 0
    C_deg = 0
    D_deg = 0

    # Stores current XY position
    X_pos = 0
    Y_pos = 0

    # Ratios between steps and degrees also sets clockwise rotation
    microstep = 0.25
    axis_A_deg_to_step = 1/(1.8 * microstep * 20/90)
    axis_B_deg_to_step = 1/(1.8 * microstep * 20/70)

    # Link lengths (in mm)
    a1 = 479.43
    a2 = 412.75

    def __init__(self, com_port):
        self.com_port = com_port

    # Connects to the robot arduino via serial
    def init(self):
        if(self.debug):
            print("Starting scara: " + self.com_port)

        self.ser = serial.Serial(self.com_port, baudrate=115200, timeout = 1)
        time.sleep(0.1)
        self.ser.flushInput()
        time.sleep(0.1)

        self.waitForResponse()

        if(self.debug):
            print("COM port opened")

    # Move individual axis by degrees
    def moveAxisATo(self, degrees):
        steps = degrees * self.axis_A_deg_to_step
        command = "M20 A%d" % steps
        self.sendCommand(command)
        self.A_deg = degrees
    
    def moveAxisBTo(self, degrees):
        steps = degrees * self.axis_B_deg_to_step
        command = "M20 B%d" % steps
        self.sendCommand(command)
        self.B_deg = degrees

    def moveAxisABTo(self, A_degrees, B_degrees):
        A_steps = A_degrees * self.axis_A_deg_to_step
        B_steps = B_degrees * self.axis_B_deg_to_step
        command = "M20 A%d B%d" % (A_steps, B_steps)
        self.sendCommand(command)
        self.A_deg = A_degrees
        self.B_deg = B_degrees
    
    # Move individual axis to set coordinates
    def moveToXY(self, x, y):
        q1, q2 = ik.calculateNegativeDeg(x, y, self.a1, self.a2) # Calculate ik
        self.A_deg = q1
        self.B_deg = q2
        A_steps = q1 * self.axis_A_deg_to_step
        B_steps = q2 * self.axis_B_deg_to_step
        command = "M20 A%d B%d" % (A_steps, B_steps)
        self.sendCommand(command)
        self.X_pos = x
        self.Y_pos = y
    
    # Move axis at correct speeds (mm per second)
    def smoothMoveToXY(self, x, y, speed):
        # Calculate ik
        q1, q2 = ik.calculateNegativeDeg(x, y, self.a1, self.a2)

        # Calc speed
        d = math.sqrt((self.X_pos - x)**2 + (self.Y_pos - y)**2)
        print("Distance: ", d)
        t = d / speed

        # Set speed
        A_speed = (abs(q1 - self.A_deg)) / t
        B_speed = (abs(q2 - self.B_deg)) / t
        self.setAxisABMaxSpeed(A_speed, B_speed)
        
        print(q1, q2)

        # Send move command
        A_steps = q1 * self.axis_A_deg_to_step
        B_steps = q2 * self.axis_B_deg_to_step
        command = "M20 A%d B%d" % (A_steps, B_steps)
        self.sendCommand(command)
        self.X_pos = x
        self.Y_pos = y
        self.A_deg = q1
        self.B_deg = q2


    # Set individual axis max speeds (in degrees)
    def setAxisABMaxSpeed(self, speed_A, speed_B):
        A_speed_steps = speed_A * self.axis_A_deg_to_step
        B_speed_steps = speed_B * self.axis_B_deg_to_step
        command = "M25 A%d B%d" % (A_speed_steps, B_speed_steps)
        self.sendCommand(command)

    # Set individual axis max speeds (in degrees)
    def setAxisABAccel(self, accel_A, accel_B):
        A_accel_steps = accel_A * self.axis_A_deg_to_step
        B_accel_steps = accel_B * self.axis_B_deg_to_step
        command = "M26 A%d B%d" % (A_accel_steps, B_accel_steps)
        self.sendCommand(command)

    # Resets the current axis rotation (in degrees)
    def setAxisABCurrentRot(self, A_degrees, B_degrees):
        self.A_deg = A_degrees
        self.B_deg = B_degrees
        A_steps = A_degrees * self.axis_A_deg_to_step
        B_steps = B_degrees * self.axis_B_deg_to_step
        command = "M27 A%d B%d" % (A_steps, B_steps)
        self.sendCommand(command)

    # Sets the move rate
    def setMoveFeed(self, feedrate):
        command = "M20 F%d" % feedrate
        self.sendCommand(command)

    # Sets the axis acceleration
    # Turns on or off debug messages
    def debugOn(self):
        self.debug = True

    def debugOff(self):
        self.debug = False

    # Send command over serial and wait for ok
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