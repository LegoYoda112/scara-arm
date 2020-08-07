import scara

arm = scara.Scara("COM7")
arm.debugOn()
arm.init()
arm.setMoveFeed(200)

arm.moveAxisATo(100)
arm.moveAxisBTo(-100)
arm.moveAxisABTo(420,0)
print(arm.A_deg)