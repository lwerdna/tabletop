#!/usr/bin/env python

# importing pygal
import pygal
import numpy
 
plants_to_payout = {
    0: 10,
    1: 22,
    2: 33,
    3: 44,
    4: 54,
    5: 64,
    6: 73,
    7: 82,
    8: 90,
    9: 98,
    10: 105,
    11: 112,
    12: 118,
    13: 124,
    14: 129,
    15: 134,
    16: 138,
    17: 142,
    18: 145,
    19: 148,
    20: 150
}

chart = pygal.Bar()
chart.title = 'Payouts'       
chart.x_labels = [str(x) for x in plants_to_payout]
chart.add(None, plants_to_payout.values())
chart.render_to_file('./payout-graph.svg')


