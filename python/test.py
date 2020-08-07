import scara

arm = scara.Scara("COM7")
arm.debugOn()
arm.init()
arm.setMoveFeed(200)