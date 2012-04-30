#!/usr/bin/env python
# coding: utf-8

"""
    python-ping unittests
    ~~~~~~~~~~~~~~~~~~~~~
    
    Note that ICMP messages can only be send from processes running as root.
    So you must run this tests also as root, e.g.:
    
        .../python-ping$ sudo python tests.py
    
    :homepage: https://github.com/jedie/python-ping/
    :copyleft: 1989-2011 by the python-ping team, see AUTHORS for more details.
    :license: GNU GPL v2, see LICENSE for more details.
"""

import socket
import unittest

from ping import Ping, is_valid_ip4_address, to_ip


class PingTest(Ping):
    """
    Used in TestPythonPing for check if print methods are called.
    This is also a way how to subclass Ping ;)
    """
    def __init__(self, *args, **kwargs):
        self.start_call_count = 0
        self.unknown_host_call_count = 0
        self.success_call_count = 0
        self.failed_call_count = 0
        self.exit_call_count = 0
        super(PingTest, self).__init__(*args, **kwargs)

    def print_start(self):
        self.start_call_count += 1

    def print_unknown_host(self, e):
        self.unknown_host_call_count += 1

    def print_success(self, delay, ip, packet_size, ip_header, icmp_header):
        self.success_call_count += 1

    def print_failed(self):
        self.failed_call_count += 1

    def print_exit(self):
        self.exit_call_count += 1


class TestPythonPing(unittest.TestCase):
    def testIp4AddrPositives(self):
        self.assertTrue(is_valid_ip4_address('0.0.0.0'))
        self.assertTrue(is_valid_ip4_address('1.2.3.4'))
        self.assertTrue(is_valid_ip4_address('12.34.56.78'))
        self.assertTrue(is_valid_ip4_address('255.255.255.255'))

    def testIp4AddrNegatives(self):
        self.assertFalse(is_valid_ip4_address('0.0.0.0.0'))
        self.assertFalse(is_valid_ip4_address('1.2.3'))
        self.assertFalse(is_valid_ip4_address('a2.34.56.78'))
        self.assertFalse(is_valid_ip4_address('255.255.255.256'))

    def testDestAddr1(self):
        self.assertTrue(is_valid_ip4_address(to_ip('www.wikipedia.org')))
        self.assertRaises(socket.gaierror, to_ip, ('www.doesntexist.tld'))

    def testDestAddr2(self):
        self.assertTrue(to_ip('10.10.10.1'))
        self.assertTrue(to_ip('10.10.010.01'))
        self.assertTrue(to_ip('10.010.10.1'))

    def test_init_only(self):
        p = PingTest("www.google.com")
        self.assertEqual(p.start_call_count, 1)
        self.assertEqual(p.unknown_host_call_count, 0)
        self.assertEqual(p.success_call_count, 0)
        self.assertEqual(p.failed_call_count, 0)
        self.assertEqual(p.exit_call_count, 0)

    def test_do_one_ping(self):
        p = PingTest("www.google.com")
        p.do()
        self.assertEqual(p.send_count, 1)
        self.assertEqual(p.receive_count, 1)

        self.assertEqual(p.start_call_count, 1)
        self.assertEqual(p.unknown_host_call_count, 0)
        self.assertEqual(p.success_call_count, 1)
        self.assertEqual(p.failed_call_count, 0)
        self.assertEqual(p.exit_call_count, 0)

    def test_do_one_failed_ping(self):
        p = PingTest("www.doesntexist.tld")
        self.assertEqual(p.start_call_count, 0)
        self.assertEqual(p.unknown_host_call_count, 1)
        self.assertEqual(p.success_call_count, 0)
        self.assertEqual(p.failed_call_count, 0)
        self.assertEqual(p.exit_call_count, 0)

    def test_run_ping(self):
        p = PingTest("www.google.com")
        p.run(count=2)
        self.assertEqual(p.send_count, 2)
        self.assertEqual(p.receive_count, 2)

        self.assertEqual(p.start_call_count, 1)
        self.assertEqual(p.unknown_host_call_count, 0)
        self.assertEqual(p.success_call_count, 2)
        self.assertEqual(p.failed_call_count, 0)
        self.assertEqual(p.exit_call_count, 1)

    def test_run_failed_pings(self):
        p = PingTest("www.google.com", timeout=0.01)
        p.run(count=2)
        self.assertEqual(p.send_count, 2)
        self.assertEqual(p.receive_count, 0)

        self.assertEqual(p.start_call_count, 1)
        self.assertEqual(p.unknown_host_call_count, 0)
        self.assertEqual(p.success_call_count, 0)
        self.assertEqual(p.failed_call_count, 2)
        self.assertEqual(p.exit_call_count, 1)


if __name__ == '__main__':
    unittest.main()

