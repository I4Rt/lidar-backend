from threading import Thread
import socket

class DeviceThread(Thread):
    
    def __init__(self, target=None, args=(), kwargs={}):
        Thread.__init__(self, target, args, kwargs)
        self._target = target
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return