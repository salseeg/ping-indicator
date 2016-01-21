#!/usr/bin/env python


import time
import math
import socket
import signal
import threading
import Queue
import random
import sys

sys.path.append('/usr/share/ping-indicator/python/')

from ping import Ping, is_valid_ip4_address
import conf
import data_exch

PING_FREQUENCY = 1  # HZ


def signal_handler(a, b):
    global daemon
    daemon.quit()
    sys.exit(0)


def make_ping_object(h, ping_id):
    timeout = 500
    if not is_valid_ip4_address(h):
        try:
            h = socket.gethostbyname(h)
        except:
            return False
    # print "ping_id = {}\n".format(ping_id)
    return Ping(h, timeout, own_id=ping_id)


class PingThread(threading.Thread):
    def __init__(self, hostname, queue, quit_event, thread_id):
        threading.Thread.__init__(self)
        self.q = queue
        self.hostname = hostname
        self.host = make_ping_object(hostname, thread_id)
        self.quit_event = quit_event
        self.thread_id = thread_id
        self.counter = random.randint(900, 1800)

    def run(self):
        while not self.quit_event.is_set():
            if self.counter < 0:
                self.host = make_ping_object(self.hostname, self.thread_id)
                self.counter = random.randint(900, 1800)
            try:
                delay = self.host.do()
                self.q.put((self.hostname, delay))
            except:
                self.q.put((self.hostname, -1))
                delay = 10
            to_sleep = 1000 / PING_FREQUENCY
            to_sleep -= delay
            to_sleep = max(to_sleep, 0)
            self.counter -= 1
            time.sleep(to_sleep / 1000)


class PingIndicatorDaemon:
    def __init__(self, hostnames, user):
        self.hostnames = hostnames
        self.user = user
        self.quit_event = threading.Event()
        self.quit_event.clear()
        self.q = Queue.Queue()
        self.threads = [PingThread(h, self.q, self.quit_event, random.randint(333, 32333)) for h in hostnames]

    def main(self):
        [t.start() for t in self.threads]
        time.sleep(0.200)
        while not self.quit_event.is_set():
            delays = dict([(h, -1) for h in self.hostnames])
            while True:
                try:
                    (host, delay) = self.q.get_nowait()
                    delays[host] = delay
                except Queue.Empty:
                    break

            self.show_results([(h, delays[h]) for h in self.hostnames])

            to_sleep = 1000 / PING_FREQUENCY
            to_sleep = max(to_sleep, 0)
            time.sleep(to_sleep / 1000)


        # def init_pinger(self, hostnames):
        # self.hosts = [ make_ping_object(h) for h in hostnames ]
        # self.hosts = []

    def show_results(self, delays):
        data = data_exch.Data_Exch(self.user)
        data.write(delays)

    def quit(self):
        self.quit_event.set()


if __name__ == "__main__":
    user = sys.argv[1]

    if len(user) > 0:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)

        c = conf.Conf(user)

        daemon = PingIndicatorDaemon(c.servers, user)
        daemon.main()
