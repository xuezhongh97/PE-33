# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:07:16 2018

@author: Paul
"""

from Being import *
from Building import *
from Entities import *
from Simulation import *
from Zone import *

simulation=Simulation()
simulation.focus_force()
simulation.lift()
simulation.mainloop()