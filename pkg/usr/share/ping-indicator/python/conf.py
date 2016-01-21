#!/usr/bin/env python
# coding: utf-8


import os


class Conf:
    def __init__(self):
        self.filename = os.path.expanduser("~/.ping-indicator/conf")
        self.servers = []
        self.read()

    def read(self):
        if os.path.exists(self.filename):
            servers = list()
            f = open(self.filename, "r")
            for line in f:
                servers.append(line.strip())
            self.servers = servers
            f.close()
        else:
            self.servers = ["8.8.8.8", "google.com", "ya.ru"]
        return self.servers

    def write(self):
        if os.path.exists(os.path.dirname(self.filename)):
            pass
        else:
            os.mkdir(os.path.dirname(self.filename))

        f = open(self.filename, "w")
        for s in self.servers:
            f.write(s + "\n")
        f.close()

    def set_servers(self, text):
        self.servers = []
        strs = text.split("\n")
        for s in strs:
            s = s.strip()
            if s != "":
                self.servers.append(s)
        self.write()
