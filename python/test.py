import scara

arm = scara.Scara("COM7")
arm.debugOn()
arm.init()
arm.setAxisABMaxSpeed(90,90)
arm.setAxisABAccel(70,70)

arm.moveAxisABTo(90,-90)
arm.moveAxisABTo(0,0)
