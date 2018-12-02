from threading import Timer

class FrameTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args[0]
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        if(not self.args['acknowledged']):
            self.is_running = False
            self.start()
            print('sending from timer..................')
            self.function(self.args['packet'])

    def start(self):
        if (not self.args['acknowledged']):
            if not self.is_running:
                self._timer = Timer(self.interval, self._run)
                self._timer.start()
                self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False