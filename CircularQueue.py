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
