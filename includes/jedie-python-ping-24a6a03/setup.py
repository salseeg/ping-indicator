#!/usr/bin/env python
# coding: utf-8

"""
    distutils setup
    ~~~~~~~~~~~~~~~

    :homepage: https://github.com/jedie/python-ping/
    :copyleft: 1989-2011 by the python-ping team, see AUTHORS for more details.
    :license: GNU GPL v2, see LICENSE for more details.
"""

import os
import subprocess
import sys
import time
import warnings

from setuptools import setup, find_packages, Command

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


#VERBOSE = True
VERBOSE = False

def _error(msg):
    if VERBOSE:
        warnings.warn(msg)
    return ""

def get_version_from_git():
    try:
        process = subprocess.Popen(
            # %ct: committer date, UNIX timestamp
            ["/usr/bin/git", "log", "--pretty=format:%ct-%h", "-1", "HEAD"],
            shell=False, cwd=PACKAGE_ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except Exception, err:
        return _error("Can't get git hash: %s" % err)

    process.wait()
    returncode = process.returncode
    if returncode != 0:
        return _error(
            "Can't get git hash, returncode was: %r"
            " - git stdout: %r"
            " - git stderr: %r"
            % (returncode, process.stdout.readline(), process.stderr.readline())
        )

    output = process.stdout.readline().strip()
    try:
        raw_timestamp, hash = output.split("-", 1)
        timestamp = int(raw_timestamp)
    except Exception, err:
        return _error("Error in git log output! Output was: %r" % output)

    try:
        timestamp_formatted = time.strftime("%Y.%m.%d", time.gmtime(timestamp))
    except Exception, err:
        return _error("can't convert %r to time string: %s" % (timestamp, err))

    return "%s.%s" % (timestamp_formatted, hash)


# convert creole to ReSt on-the-fly, see also:
# https://code.google.com/p/python-creole/wiki/UseInSetup
try:
    from creole.setup_utils import get_long_description
except ImportError:
    if "register" in sys.argv or "sdist" in sys.argv or "--long-description" in sys.argv:
        etype, evalue, etb = sys.exc_info()
        evalue = etype("%s - Please install python-creole >= v0.8 -  e.g.: pip install python-creole" % evalue)
        raise etype, evalue, etb
    long_description = None
else:
    long_description = get_long_description(PACKAGE_ROOT)


def get_authors():
    authors = []
    try:
        f = file(os.path.join(PACKAGE_ROOT, "AUTHORS"), "r")
        for line in f:
            if not line.strip().startswith("*"):
                continue
            if "--" in line:
                line = line.split("--", 1)[0]
            authors.append(line.strip(" *\r\n"))
        f.close()
        authors.sort()
    except Exception, err:
        authors = "[Error: %s]" % err
    return authors


setup(
    name='python-ping',
    version=get_version_from_git(),
    description='A pure python ICMP ping implementation using raw sockets.',
    long_description=long_description,
    author=get_authors(),
    maintainer="Jens Diemer",
    maintainer_email="python-ping@jensdiemer.de",
    url='https://github.com/jedie/python-ping/',
    keywords="ping icmp network latency",
    packages=find_packages(),
    include_package_data=True, # include package data under svn source control
    zip_safe=False,
    scripts=["ping.py"],
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
#        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking :: Monitoring",
    ],
    test_suite="tests",
)
