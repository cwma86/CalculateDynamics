#! /usr/bin/env python
import argparse
import socketserver


class options():
    def __init__(self):
        parser = argparse.ArgumentParser(description='prints hello world')
        parser.add_argument('--paramsFile', dest='paramsFile', type=str, 
        nargs='?', help='file location for params')
        args = parser.parse_args()
        self.inputText = args.paramsFile


class CircularQueue:
    def __init__(self, maxQueueSize):
        self.queueSize = maxQueueSize
        self.objectList = [None] * maxQueueSize
        self.head = 0
        self.tail = 0

    def dequeue(self):
        firstPosition = self.objectList[self.head]
        self.objectList[self.head] = None
        if not self.head == self.tail:
            if self.head + 1 > self.queueSize - 1:
                self.head = 0
            else:
                self.head = self.head + 1
        else:
            self.head = 0
            self.tail = 0        
        return firstPosition

    def enqueue(self, object):
        if self.head == self.tail:
            if self.objectList[self.head]:
                # setting second value of the queue
                if(self.tail + 1 > self.queueSize - 1):
                    self.tail = 0
                else:
                    self.tail = self.tail + 1
                self.objectList[self.tail] = object
            else:
                # Set initial value of the queue
                self.objectList[self.head] = object
        else:
            if(self.tail + 1 > self.queueSize - 1):
                if self.head == 0:
                    self.dequeue()
                self.tail = 0
            else:
                if self.tail + 1 == self.head:
                    self.dequeue()
                self.tail = self.tail + 1
            self.objectList[self.tail] = object
    

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    TCP Server
    """
    queue = CircularQueue(5)

    def handle(self):
        self.data = self.request.recv(1024)
        print("{} sent:".format(self.client_address[0]))
        print("data %s" %self.data)
        data = self.data.decode("ASCII")
        dataList = data.split()
        if len(dataList) == 4:
            receivedPosition = position(dataList[0], dataList[1],
                                        dataList[2], dataList[3])
            self.queue.enqueue(receivedPosition)
            # TODO calculate average velocity 
            # TODO calclate average acceleration
        else:
            print("Warning Invalid length = %s" %len(dataList))
        acknowledge = "ACK"
        self.request.sendall(bytes(acknowledge + "\n", "ASCII"))

# TODO make this class shared between the two projects
class position:
    def __init__(self, x, y, z, time):
        self.x = x
        self.y = y
        self.z = z
        self.time = time

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
    # TODO make host/port configurable
    inputArgs = options()
    HOST = "127.0.0.1"
    PORT = 9999
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)
    tcp_server.serve_forever()

if __name__ == "__main__":
    main()
