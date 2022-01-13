from threading import Thread, Event
import threading
import time, sys
import random


class ThreadUP(Thread):

    returnValue: bool

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None, returnValue=False):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.returnValue = returnValue
        self._return = None

    def __join(self, *args):
        if self.is_alive():
            Thread.join(self, *args)
        if self.returnValue:
            return self._return

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        return self.__join(*args)

    def startJoin(self, *args):
        self.start()
        return self.__join(*args)

class Test():

    def __init__(self) -> None:
        self.val = random.randint(0, 500)

    def returnVal(self):
        return self.val

print(f"start at {time.strftime('%X')}")

def test(time_n: int):
    for i in range(0, time_n):
        time.sleep(1)
    return time_n

task1 = ThreadUP(target=Test, returnValue=True)
task2 = ThreadUP(target=lambda: test(10), returnValue=True).startJoin()

try:
    task1.start()
except:
    print(sys.exc_info()[0])


print(task1.join().returnVal())
print(task2)


print(f"finished at {time.strftime('%X')}")