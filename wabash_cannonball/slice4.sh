#!/bin/sh

convert -crop 792x612+0+0 ./map2.png ./map2_1.png
convert -crop 792x612+792+0 ./map2.png ./map2_2.png
convert -crop 792x612+0+612 ./map2.png ./map2_3.png
convert -crop 792x612+792+612 ./map2.png ./map2_4.png
