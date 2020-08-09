import scara
import time

arm = scara.Scara("COM7")
arm.debugOn()
arm.init()
arm.setAxisABMaxSpeed(30,30)
arm.setAxisABAccel(20,20)
arm.setAxisABCurrentRot(-90, 0)

arm.moveToXY(0,-800)

time.sleep(1)
## Smooth move
arm.setAxisABAccel(500,500)
print("CORNER 1 ----------------")
arm.smoothMoveToXY(0, -700, 50)
#time.sleep(1)
print("CORNER 2 ----------------")
arm.smoothMoveToXY(0, -600, 50)
#time.sleep(1)
print("CORNER 3 ----------------")
arm.smoothMoveToXY(0, -500, 50)
#time.sleep(1)
print("CORNER 4 ----------------")
arm.smoothMoveToXY(0, -400, 50)
#time.sleep(1)

arm.setAxisABMaxSpeed(30,30)
arm.setAxisABAccel(20,20)
arm.moveAxisABTo(-90,0)