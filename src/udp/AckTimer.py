from threading import Timer

class AckTimer(object):
    

    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = 0.05
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        if self.is_running:
            print("stopping the timer for ", self.args)
            self._timer.cancel()
            self.is_running = False

# import time
# def __init__(self,interval):
#     self._timer     = None
#     self.interval   = interval
#     self.is_running = False

# def start(self):
#     self.is_running = True
#     countdown(self.interval)
# def stop(self):
#    self.is_running = False
   

    
# def reset(self):
#     self.start()

# def countdown(slef,interval):
#     while interval:
#         mins, secs = divmod(interval, 60)
#         timeformat = '{:02d}:{:02d}'.format(mins, secs)
#         print(timeformat, end='\r')
#         time.sleep(1)
#         interval -= 1
#     print('Time out\n\n\n\n\n')