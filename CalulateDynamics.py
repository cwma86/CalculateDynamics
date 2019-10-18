#! /usr/bin/env python
import argparse
from ValueGenerate import position


class options():
    def __init__(self):
        parser = argparse.ArgumentParser(description='prints hello world')
        parser.add_argument('--paramsFile', dest='paramsFile', type=str, 
        nargs='?', help='file location for params')
        args = parser.parse_args()
        self.inputText = args.paramsFile

class velocitiy:
    def __init__(self, initPosition, finalPosition):
        timeDelta = finalPosition.time - initPosition.time
        if abs(timeDelta) > 1e-4:
            positionDelta = finalPosition.x - initPosition.x
            self.x = positionDelta / timeDelta 
            positionDelta = finalPosition.y - initPosition.y
            self.y = positionDelta / timeDelta 
            positionDelta = finalPosition.z - initPosition.z
            self.z = positionDelta / timeDelta 
        else:
            print("Invalid initial and final position time delta = %s" % timeDelta)


def main():
    inputArgs = options()
    # TODO receive data via tcp 
    # TODO store positon
    # TODO calculate velocity
    # TODO calculate average velocity (circular queue)
    # TODO calculate acceleration

if __name__ == "__main__":
    main()
