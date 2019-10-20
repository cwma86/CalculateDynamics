class Velocity:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x 
        self.y = y
        self.z = z 

    def __add__(self, velocity):
        x = self.x + velocity.x
        y = self.y + velocity.y
        z = self.z + velocity.z
        return Velocity(x,y,z)
    
    def __truediv__(self, denominator=1):
        if not denominator == 0.0:
            x = self.x / denominator
            y = self.y / denominator
            z = self.z / denominator
        else:
            print("Invalid denominator = %f" % denominator)
            x = 0.0
            y = 0.0
            z = 0.0
        return Velocity(x,y,z)
        
    def setVelocity(self, finalPosition, initPosition):
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
            