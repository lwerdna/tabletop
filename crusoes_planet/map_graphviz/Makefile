#all: map_dot.png map_circo.png map_fdp.png map_neato.png map_twopi.png map_osage.png map_patchwork.png map_dot.svg
all: map_dot.png map_dot.svg

map_dot.svg: map.dot
	dot -Tsvg map.dot -o map_dot.svg

map_dot.png: map.dot
	dot -Tpng map.dot -o map_dot.png

map_circo.png: map.dot
	circo -Tpng map.dot -o map_circo.png

map_fdp.png: map.dot
	fdp -Tpng map.dot -o map_fdp.png

#map_sfdp.png: map.dot
#	sfdp -Tpng map.dot -o map_sfdp.png

map_neato.png: map.dot
	neato -Tpng map.dot -o map_neato.png

map_twopi.png: map.dot
	twopi -Tpng map.dot -o map_twopi.png

map_osage.png: map.dot
	osage -Tpng map.dot -o map_osage.png

map_patchwork.png: map.dot
	patchwork -Tpng map.dot -o map_patchwork.png

map.dot: data.csv data2dot.py
	./data2dot.py > map.dot

clean:
	rm -rf map*.png map_dot.svg map.dot
