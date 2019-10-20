#! /usr/bin/env python
import argparse
import socketserver
import CircularQueue
from Position import Position
from Velocity import Velocity


positionQueue = CircularQueue.CircularQueue(10)
velocityQueue = CircularQueue.CircularQueue(10)


class options():
    def __init__(self):
        parser = argparse.ArgumentParser(description='Receives position data over TCP and \
                                                      calculates velocity and acceleration')
        parser.add_argument('--host', dest='host', type=str, 
        nargs='?', help='Host IP address that data will be received')
        parser.add_argument('--port', '-p', dest='port', type=int, 
        nargs='?', help='Host port that data will be received')
        args = parser.parse_args()
        if args.host:
            self.host = args.host
        else:
            self.host = "127.0.0.1"
        if args.port:
            self.port = args.port
        else:
            self.port = 9999
 

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    TCP Server
    """
    def handle(self):
        self.data = self.request.recv(1024)
        print("{} sent:".format(self.client_address[0]))
        print("data %s" % self.data)
        data = self.data.decode("ASCII")
        dataList = data.split()
        CalculateDynamics(dataList)


def CalcualteAverageVelocty():
    index =  velocityQueue.head 
    velocitySum = Velocity()
    numOfVelocitiesInQueue = 1
    velocitySum = velocitySum + velocityQueue.objectList[index]

    while not index == velocityQueue.tail:
        index = index + 1
        numOfVelocitiesInQueue = numOfVelocitiesInQueue + 1
        # Handle queue rollover
        if index > velocityQueue.queueSize - 1:
            index = 0

        velocitySum = velocitySum + velocityQueue.objectList[index]
    averageVelocity = velocitySum / numOfVelocitiesInQueue
    return averageVelocity

def CalculateDynamics(positionDataList):
    kMaxVelocityTimeDelta = 10
    if len(positionDataList) == 4:
        receivedPosition = Position(float(positionDataList[0]), float(positionDataList[1]),
                                    float(positionDataList[2]), float(positionDataList[3]))
        # Clean up the position queue removing any invalid or old positions
        while positionQueue.objectList[positionQueue.head]:
            headTimeDelta = receivedPosition.time - positionQueue.objectList[positionQueue.head].time
            if headTimeDelta > kMaxVelocityTimeDelta or headTimeDelta <= 0:
                positionQueue.dequeue()
                velocityQueue.dequeue()
            else:
                break
        positionQueue.enqueue(receivedPosition)
        # calculate velocity if atleast 2 positions existS
        if not positionQueue.tail == positionQueue.head:
            instVelocity = Velocity()
            instVelocity.setVelocity(positionQueue.objectList[positionQueue.tail], 
                                     positionQueue.objectList[positionQueue.tail -1])
            velocityQueue.enqueue(instVelocity)
            print("Instaneous velocity x = " + str(velocityQueue.objectList[velocityQueue.tail].x))

            # calculate average velocity if atleast 2 velocities exist
            if not velocityQueue.tail == velocityQueue.head:
                averageVelocity = CalcualteAverageVelocty()
                print("average velocity x = %f " % averageVelocity.x)

    else:
        print("Warning Invalid length = %s" %len(positionDataList))

def main():
    inputArgs = options()
    tcp_server = socketserver.TCPServer((inputArgs.host, inputArgs.port), Handler_TCPServer)
    tcp_server.serve_forever()

if __name__ == "__main__":
    main()
