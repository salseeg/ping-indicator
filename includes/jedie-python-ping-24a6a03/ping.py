#!/usr/bin/env python
# coding: utf-8

"""
    A pure python ping implementation using raw sockets.

    Note that ICMP messages can only be send from processes running as root
    (in Windows, you must run this script as 'Administrator').

    Bugs are naturally mine. I'd be glad to hear about them. There are
    certainly word - size dependencies here.
    
    :homepage: https://github.com/jedie/python-ping/
    :copyleft: 1989-2011 by the python-ping team, see AUTHORS for more details.
    :license: GNU GPL v2, see LICENSE for more details.
"""


import os
import select
import signal
import socket
import struct
import sys
import time


if sys.platform.startswith("win32"):
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time


# ICMP parameters
ICMP_ECHOREPLY = 0 # Echo reply (per RFC792)
ICMP_ECHO = 8 # Echo request (per RFC792)
ICMP_MAX_RECV = 2048 # Max size of incoming buffer

MAX_SLEEP = 1000


def calculate_checksum(source_string):
    """
    A port of the functionality of in_cksum() from ping.c
    Ideally this would act on the string as a series of 16-bit ints (host
    packed), but this works.
    Network data is big-endian, hosts are typically little-endian
    """
    countTo = (int(len(source_string) / 2)) * 2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    loByte = 0
    hiByte = 0
    while count < countTo:
        if (sys.byteorder == "little"):
            loByte = source_string[count]
            hiByte = source_string[count + 1]
        else:
            loByte = source_string[count + 1]
            hiByte = source_string[count]
        sum = sum + (ord(hiByte) * 256 + ord(loByte))
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if countTo < len(source_string): # Check for odd length
        loByte = source_string[len(source_string) - 1]
        sum += ord(loByte)

    sum &= 0xffffffff # Truncate sum to 32 bits (a variance from ping.c, which
                      # uses signed ints, but overflow is unlikely in ping)

    sum = (sum >> 16) + (sum & 0xffff)    # Add high 16 bits to low 16 bits
    sum += (sum >> 16)                    # Add carry from above (if any)
    answer = ~sum & 0xffff                # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer


def is_valid_ip4_address(addr):
    parts = addr.split(".")
    if not len(parts) == 4:
        return False
    for part in parts:
        try:
            number = int(part)
        except ValueError:
            return False
        if number > 255:
            return False
    return True

def to_ip(addr):
    if is_valid_ip4_address(addr):
        return addr
    return socket.gethostbyname(addr)


class Ping(object):
    def __init__(self, destination, timeout=1000, packet_size=55, own_id=None):
        self.destination = destination
        self.timeout = timeout
        self.packet_size = packet_size
        if own_id is None:
            self.own_id = os.getpid() & 0xFFFF
        else:
            self.own_id = own_id

        try:
            # FIXME: Use destination only for display this line here? see: https://github.com/jedie/python-ping/issues/3
            self.dest_ip = to_ip(self.destination)
        except socket.gaierror as e:
            self.print_unknown_host(e)
        else:
            self.print_start()

        self.seq_number = 0
        self.send_count = 0
        self.receive_count = 0
        self.min_time = 999999999
        self.max_time = 0.0
        self.total_time = 0.0

    #--------------------------------------------------------------------------

    def print_start(self):
        print("\nPYTHON-PING %s (%s): %d data bytes" % (self.destination, self.dest_ip, self.packet_size))

    def print_unknown_host(self, e):
        print("\nPYTHON-PING: Unknown host: %s (%s)\n" % (self.destination, e.args[1]))
        sys.exit(-1)

    def print_success(self, delay, ip, packet_size, ip_header, icmp_header):
        if ip == self.destination:
            from_info = ip
        else:
            from_info = "%s (%s)" % (self.destination, ip)

        print("%d bytes from %s: icmp_seq=%d ttl=%d time=%.1f ms" % (
            packet_size, from_info, icmp_header["seq_number"], ip_header["ttl"], delay)
        )
        #print("IP header: %r" % ip_header)
        #print("ICMP header: %r" % icmp_header)

    def print_failed(self):
        print("Request timed out.")

    def print_exit(self):
        print("\n----%s PYTHON PING Statistics----" % (self.destination))

        lost_count = self.send_count - self.receive_count
        #print("%i packets lost" % lost_count)
        lost_rate = float(lost_count) / self.send_count * 100.0

        print("%d packets transmitted, %d packets received, %0.1f%% packet loss" % (
            self.send_count, self.receive_count, lost_rate
        ))

        if self.receive_count > 0:
            print("round-trip (ms)  min/avg/max = %0.3f/%0.3f/%0.3f" % (
                self.min_time, self.total_time / self.receive_count, self.max_time
            ))

        print("")

    #--------------------------------------------------------------------------

    def signal_handler(self, signum, frame):
        """
        Handle print_exit via signals
        """
        self.print_exit()
        print("\n(Terminated with signal %d)\n" % (signum))
        sys.exit(0)

    def setup_signal_handler(self):
        signal.signal(signal.SIGINT, self.signal_handler)   # Handle Ctrl-C
        if hasattr(signal, "SIGBREAK"):
            # Handle Ctrl-Break e.g. under Windows 
            signal.signal(signal.SIGBREAK, self.signal_handler)

    #--------------------------------------------------------------------------

    def header2dict(self, names, struct_format, data):
        """ unpack the raw received IP and ICMP header informations to a dict """
        unpacked_data = struct.unpack(struct_format, data)
        return dict(zip(names, unpacked_data))

    #--------------------------------------------------------------------------

    def run(self, count=None, deadline=None):
        """
        send and receive pings in a loop. Stop if count or until deadline.
        """
        self.setup_signal_handler()

        while True:
            delay = self.do()

            self.seq_number += 1
            if count and self.seq_number >= count:
                break
            if deadline and self.total_time >= deadline:
                break

            if delay == None:
                delay = 0

            # Pause for the remainder of the MAX_SLEEP period (if applicable)
            if (MAX_SLEEP > delay):
                time.sleep((MAX_SLEEP - delay) / 1000.0)

        self.print_exit()

    def do(self):
        """
        Send one ICMP ECHO_REQUEST and receive the response until self.timeout
        """
        try: # One could use UDP here, but it's obscure
            current_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        except socket.error, (errno, msg):
            if errno == 1:
                # Operation not permitted - Add more information to traceback
                etype, evalue, etb = sys.exc_info()
                evalue = etype(
                    "%s - Note that ICMP messages can only be send from processes running as root." % evalue
                )
                raise etype, evalue, etb
            raise # raise the original error

        send_time = self.send_one_ping(current_socket)
        if send_time == None:
            return
        self.send_count += 1

        receive_time, packet_size, ip, ip_header, icmp_header = self.receive_one_ping(current_socket)
        current_socket.close()

        if receive_time:
            self.receive_count += 1
            delay = (receive_time - send_time) * 1000.0
            self.total_time += delay
            if self.min_time > delay:
                self.min_time = delay
            if self.max_time < delay:
                self.max_time = delay

            self.print_success(delay, ip, packet_size, ip_header, icmp_header)
            return delay
        else:
            self.print_failed()

    def send_one_ping(self, current_socket):
        """
        Send one ICMP ECHO_REQUEST
        """
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        checksum = 0

        # Make a dummy header with a 0 checksum.
        header = struct.pack(
            "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number
        )

        padBytes = []
        startVal = 0x42
        for i in range(startVal, startVal + (self.packet_size)):
            padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        data = bytes(padBytes)

        # Calculate the checksum on the data and the dummy header.
        checksum = calculate_checksum(header + data) # Checksum is in network order

        # Now that we have the right checksum, we put that in. It's just easier
        # to make up a new header than to stuff it into the dummy.
        header = struct.pack(
            "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number
        )

        packet = header + data

        send_time = default_timer()

        try:
            current_socket.sendto(packet, (self.destination, 1)) # Port number is irrelevant for ICMP
        except socket.error as e:
            print("General failure (%s)" % (e.args[1]))
            current_socket.close()
            return

        return send_time

    def receive_one_ping(self, current_socket):
        """
        Receive the ping from the socket. timeout = in ms
        """
        timeout = self.timeout / 1000.0

        while True: # Loop while waiting for packet or timeout
            select_start = default_timer()
            inputready, outputready, exceptready = select.select([current_socket], [], [], timeout)
            select_duration = (default_timer() - select_start)
            if inputready == []: # timeout
                return None, 0, 0, 0, 0

            receive_time = default_timer()

            packet_data, address = current_socket.recvfrom(ICMP_MAX_RECV)

            icmp_header = self.header2dict(
                names=[
                    "type", "code", "checksum",
                    "packet_id", "seq_number"
                ],
                struct_format="!BBHHH",
                data=packet_data[20:28]
            )

            if icmp_header["packet_id"] == self.own_id: # Our packet
                ip_header = self.header2dict(
                    names=[
                        "version", "type", "length",
                        "id", "flags", "ttl", "protocol",
                        "checksum", "src_ip", "dest_ip"
                    ],
                    struct_format="!BBHHHBBHII",
                    data=packet_data[:20]
                )
                packet_size = len(packet_data) - 28
                ip = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
                # XXX: Why not ip = address[0] ???
                return receive_time, packet_size, ip, ip_header, icmp_header

            timeout = timeout - select_duration
            if timeout <= 0:
                return None, 0, 0, 0, 0


def verbose_ping(hostname, timeout=1000, count=3, packet_size=55):
    p = Ping(hostname, timeout, packet_size)
    p.run(count)


if __name__ == '__main__':
    # FIXME: Add a real CLI
    if len(sys.argv) == 1:
        print "DEMO"

        # These should work:
        verbose_ping("heise.de")
        verbose_ping("google.com")

        # Inconsistent on Windows w/ ActivePython (Python 3.2 resolves correctly
        # to the local host, but 2.7 tries to resolve to the local *gateway*)
        verbose_ping("localhost")

        # Should fail with 'getaddrinfo print_failed':
        verbose_ping("foobar_url.foobar")

        # Should fail (timeout), but it depends on the local network:
        verbose_ping("192.168.255.254")

        # Should fails with 'The requested address is not valid in its context':
        verbose_ping("0.0.0.0")
    elif len(sys.argv) == 2:
        verbose_ping(sys.argv[1])
    else:
        print "Error: call ./ping.py domain.tld"
