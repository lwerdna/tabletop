# 11 x 8.5 = 2486 x 1920
# 1in = 226 (dpi)
# .5in = 113
# .75in = 169.5

tiles: water_tile_p75in.png apple_tile_p75in.png banana_tile_p75in.png grapes_tile_p75in.png egg_tile_p75in.png fish_tile_p75in.png spear_tile_p75in.png diamond_tile_p75in.png leisure_tile_p75in.png radio_cb_tile_p75in.png radio_mil_tile_p75in.png radio_t40_tile_p75in.png

# -------- water --------

water_tile_p75in.png: water.png
	convert -resize 170x170 water.png water_tile_p75in.png

apple_tile_p75in.png: apple.png
	convert -resize 170x170 apple.png apple_tile_p75in.png

banana_tile_p75in.png: banana.png
	convert -resize 170x170 banana.png banana_tile_p75in.png

grapes_tile_p75in.png: grapes.png
	convert -resize 170x170 grapes.png grapes_tile_p75in.png

egg_tile_p75in.png: egg.png
	convert -resize 170x170 egg.png egg_tile_p75in.png

fish_tile_p75in.png: fish.png
	convert -resize 170x170 fish.png fish_tile_p75in.png

spear_tile_p75in.png: spear.png
	convert -resize 170x170 spear.png spear_tile_p75in.png

diamond_tile_p75in.png: diamond.png
	convert -resize 170x170 diamond.png diamond_tile_p75in.png

leisure_tile_p75in.png: leisure.png
	convert -resize 170x170 leisure.png leisure_tile_p75in.png

radio_cb_tile_p75in.png: radio_cb.png
	convert -resize 170x170 radio_cb.png radio_cb_tile_p75in.png

radio_mil_tile_p75in.png: radio_mil.png
	convert -resize 170x170 radio_mil.png radio_mil_tile_p75in.png

radio_t40_tile_p75in.png: radio_t40.png
	convert -resize 170x170 radio_t40.png radio_t40_tile_p75in.png

clean:
	rm -rf *_tile_p75in.png
