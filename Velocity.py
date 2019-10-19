class Velocity:
    def __init__(self, finalPosition, initPosition):
        timeDelta = finalPosition.time - initPosition.time
        if abs(timeDelta) > 1e-4:
            positionDelta = finalPosition.x - initPosition.x
            self.x = positionDelta / timeDelta 
            positionDelta = finalPosition.y - initPosition.y
            self.y = positionDelta / timeDelta 
            positionDelta = finalPosition.z - initPosition.z
            self.z = positionDelta / timeDelta 
        else:
            self.x = 0.0 
            self.y = 0.0
            self.z = 0.0 

            print("Invalid initial and final position time delta = %s" % timeDelta)
