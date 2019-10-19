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

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    TCP Server
    """

    def handle(self):
        self.data = self.request.recv(1024)
        print("{} sent:".format(self.client_address[0]))
        print("data %s" %self.data)
        data = self.data.decode("ASCII")
        print(self.data)
        dataList = data.split()
        # TODO populate queue
        # TODO calculate average velocity 
        # TODO calclate average acceleration
        if len(dataList) == 4:
            receivedPosition = position(dataList[0], dataList[1],
                                        dataList[2], dataList[3])
        else:
            print("length = %s" %len(dataList))
            print("dataList")
            print(dataList)
            print(dataList[1])
        self.request.sendall("ACK from TCP Server".encode())

#TODO make this class shared between the two projects
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

class CircularQueue:
    __init__(self, maxSize):
        self.queueSize = maxSize
        self.positionList = None
        self.head = 0
        self.tail = 0

    def enqueue(self, position):
        if self.head == self.tail:
            if self.positionList[self.head]:
                # setting second value of the queue
                if(self.tail + 1 > self.queueSize - 1):
                    self.tail = 0
                else:
                    self.tail++
                self.positionList[self.tail] = position
            else:
                # Set initial value of the queue
                self.positionList[self.head] = position

        else:
            if(self.tail + 1 > self.queueSize - 1):
                self.tail = 0
            else:
                self.tail++
            if self.head == self.tail:
                # Queue is full replace oldest object
                if self.head + 1 > self.queue size - 1:
                    self.head = 0
                else:
                    self.head++
            self.positionList[self.tail] = position



            else:
                self.positionList[self.head] = position
    
    def dequeue(self, position):

def main():
    inputArgs = options()
    # TODO start TCP server
    HOST = "127.0.0.1"
    PORT = 9999
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)
    tcp_server.serve_forever()
    # TODO receive data via tcp 
    # TODO store positon
    # TODO calculate velocity
    # TODO calculate average velocity (circular queue)
    # TODO calculate acceleration

if __name__ == "__main__":
    main()
