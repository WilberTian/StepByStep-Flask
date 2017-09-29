class QueueMetaclass(type):
    def __new__(cls, name, bases, attrs):
        def inQueue(self, value):
            self.append(value)

        def deQueue(self):
            return self.pop(0)

        attrs['inQueue'] = inQueue
        attrs['deQueue'] = deQueue

        return type.__new__(cls, name, bases, attrs)

class MyQueue(list):
    __metaclass__ = QueueMetaclass
    pass

queue = MyQueue([1, 2, 3])
print queue

queue.inQueue(10)
print queue

print queue.deQueue()
