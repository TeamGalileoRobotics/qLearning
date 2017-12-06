#!/usr/bin/env python

import time
import nxt.locator
from nxt.sensor import *
from nxt.motor import *

b = nxt.locator.find_one_brick(name = 'NXT')

m = Motor(b, PORT_A)

m.reset_position(False)

print m.get_tacho().tacho_count
print m.get_tacho().rotation_count

m.turn(100, 20)
print m.get_tacho().tacho_count
print m.get_tacho().rotation_count

m.turn(100, 0)
print m.get_tacho().tacho_count
print m.get_tacho().rotation_count