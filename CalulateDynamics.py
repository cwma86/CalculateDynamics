#! /usr/bin/env python
import argparse
import socketserver
import CircularQueue
from Position import Position
from Velocity import Velocity


queue = CircularQueue.CircularQueue(10)

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

def CalculateDynamics(positionDataList):
    if len(positionDataList) == 4:
        receivedPosition = Position(float(positionDataList[0]), float(positionDataList[1]),
                                    float(positionDataList[2]), float(positionDataList[3]))
        queue.enqueue(receivedPosition)
        # TODO throw away old positions
        # TODO calculate average velocity 
        vel = Velocity(queue.objectList[queue.tail], 
                    queue.objectList[queue.tail -1])
        print(" velocity x = " + str(vel.x))
        # TODO calclate average acceleration
    else:
        print("Warning Invalid length = %s" %len(positionDataList))

def main():
    # TODO make host/port configurable
    inputArgs = options()
    tcp_server = socketserver.TCPServer((inputArgs.host, inputArgs.port), Handler_TCPServer)
    tcp_server.serve_forever()

if __name__ == "__main__":
    main()
