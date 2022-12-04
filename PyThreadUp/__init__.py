from threading import Thread
import threading, sys
from typing import Any


class ThreadUP(threading.Thread):
    def __init__(self, returnValue=False, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        self.returnValue = returnValue

    def __join(self, *args):
        if self.is_alive():
            Thread.join(self, *args)
        if self.returnValue:
            try:
                return self._return
            except:
                return None

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
    
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def join(self, *args):
        return self.__join(*args)
    
    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None
    
    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
            return self.localtrace

    def kill(self):
        self.killed = True


class ThreadManager():

    threads: dict[str, ThreadUP]

    def __init__(self) -> None:
        self.threads = {}

    def thread(self, name: str, target: Any | None, args: Any = (), returnValue: bool = False):

        self.threads[name] = ThreadUP(returnValue=returnValue, name=name, target=target, args=args)

    def start(self, name: str):

        t = self.get_thread(name)
        try:
            t.start()
        except RuntimeError as e:
            self.threads[name] = ThreadUP(name=t._name, target=t._target, args=t._args, returnValue=t.returnValue)
            self.threads[name].start()

    def join(self, name: str) -> Any | None:
        
        return self.get_thread(name).join()

    def kill(self, name: str):
        
        t = self.get_thread(name)
        t.kill()

        self.threads[name] = ThreadUP(name=t._name, target=t._target, args=t._args, returnValue=t.returnValue)

    def kill_all(self):
        
        for name, t in self.threads.items():
            t.kill()
            self.threads[name] = ThreadUP(name=t._name, target=t._target, args=t._args, returnValue=t.returnValue)

    def is_alive(self, name: str) -> bool:
        
        return self.get_thread(name).is_alive()

    def get_thread(self, name: str) -> ThreadUP:

        try:
            return self.threads[name]
        except:
            raise(f"Thread name {name} not existe")

    def get_threads(self) -> dict[str, ThreadUP]:

        return self.threads

    def remove(self, name: str):

        try:
            del self.threads[name]
        except:
            raise(f"Thread name {name} not existe")