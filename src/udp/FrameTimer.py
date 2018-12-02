from threading import Timer

class FrameTimer(object):
    def __init__(self, interval, router_addr, router_port, packet, connection):
        self._timer     = None
        self.interval   = interval
        self.router_addr = router_addr
        self.router_port = router_port
        self.connection = connection
        self.packet = packet
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.send_packet()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def send_packet(self):
        if self.packet != None:
            self.connection.sendto(self.packet.to_bytes(), (self.router_addr, self.router_port))
            self.connection.settimeout(self.timeout)
            print("sent packet from the frame timer mother fucker")

    def stop(self):
        if self.is_running:
            self._timer.cancel()
            self.is_running = False