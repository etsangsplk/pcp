#!/usr/bin/python
#
# Copyright (C) 2012 Red Hat Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#

import unittest
import pmapi
#import time
#import sys
#import argparse
from pcp import *
from ctypes import *

# some random default values
hostname = "fu.bar.com"
timezone = "UTC"
outfile = ""

def test_pmi(self, path = outfile, inherit = 0):

    print "Writing to new PCP archive:", path
    pmi = pmiLogImport(path, inherit)

    code = pmi.pmiSetHostname(hostname)
    print "pmiSetHostname:", hostname
    self.assertTrue(code >= 0)

    code = pmi.pmiSetTimezone(timezone)
    print "pmiSetTimezone:", timezone
    self.assertTrue(code >= 0)

    pmid = pmi.pmiID(60, 2, 0)
    indom = pmi.pmiInDom(60, 2)
    units = pmi.pmiUnits(0,0,0,0,0,0)

    # create a metric without instances (hinv.ncpu)
    code = pmi.pmiAddMetric("hinv.ncpu", PM_ID_NULL, PM_TYPE_U32, PM_INDOM_NULL, PM_SEM_DISCRETE, units)
    print "pmiAddMetric: hinv.ncpu"
    self.assertTrue(code >= 0)

    # give it a value
    code = pmi.pmiPutValue("hinv.ncpu", "", "42")
    print "pmiPutValue: hinv.ncpu"
    self.assertTrue(code >= 0)

    # create a metric with instances (kernel.all.load)
    code = pmi.pmiAddMetric("kernel.all.load", pmid, PM_TYPE_FLOAT, indom, PM_SEM_DISCRETE, units)
    print "pmiAddMetric: kernel.all.load"
    self.assertTrue(code >= 0)
    code = pmi.pmiAddInstance(indom, "1 minute", 1)
    print "pmiAddInstance: kernel.all.load[1 minute]"
    self.assertTrue(code >= 0)
    code = pmi.pmiAddInstance(indom, "5 minute", 5)
    print "pmiAddMetric: kernel.all.load[5 minute]"
    self.assertTrue(code >= 0)
    code = pmi.pmiAddInstance(indom, "15 minute", 15)
    print "pmiAddMetric: kernel.all.load[15 minute]"
    self.assertTrue(code >= 0)

    # give them values
    code = pmi.pmiPutValue("kernel.all.load", "1 minute", "42.01")
    print "pmiPutValue: kernel.all.load[1 minute]"
    self.assertTrue(code >= 0)
    code = pmi.pmiPutValue("kernel.all.load", "5 minute", "42.05")
    print "pmiPutValue: kernel.all.load[5 minute]"
    self.assertTrue(code >= 0)
    code = pmi.pmiPutValue("kernel.all.load", "15 minute", "42.15")
    print "pmiPutValue: kernel.all.load[15 minute]"
    self.assertTrue(code >= 0)

    del pmi

class TestSequenceFunctions(unittest.TestCase):

    def test_context(self):
        test_pmi(self, outfile)

if __name__ == '__main__':

    if (len(sys.argv) == 2):
        outfile = sys.argv[1]
    else:
        print "Usage: " + sys.argv[0] + " OutFile"
        sys.exit(1)

    sys.argv[1:] = ()

    unittest.main()
    sys.exit(main())

