from threading import Thread

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
        # return

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        return self.__join(*args)

    def startTask(self):
        self.start()
        return self