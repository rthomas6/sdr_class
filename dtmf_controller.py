#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from dtmf import dtmf
import time

fg = dtmf()
def press(num):
    label = 'set_b{}'.format(num)
    set_cmd = getattr(fg, label)
    set_cmd(1)
    time.sleep(0.5)
    set_cmd(0)
    time.sleep(0.5)
numlist = [3,2,1,2,3,3,3,2,2,2,3,9,9,3,2,1,2,3,3,3,3,2,2,3,2,1]

fg.start()

[press(x) for x in numlist]

time.sleep(5)
fg.stop()
fg.wait()