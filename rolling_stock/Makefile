#all: graph_dot.png graph_circo.png graph_fdp.png graph_neato.png graph_twopi.png graph_osage.png graph_patchwork.png graph_dot.svg
all: graph_dot.png graph_circo.png graph_fdp.png graph_neato.png graph_twopi.png graph_osage.png graph_patchwork.png

graph_dot.png: graph.dot
	dot -Tpng graph.dot -o graph_dot.png

graph_circo.png: graph.dot
	circo -Tpng graph.dot -o graph_circo.png

graph_fdp.png: graph.dot
	fdp -Tpng graph.dot -o graph_fdp.png

#graph_sfdp.png: graph.dot
#	sfdp -Tpng graph.dot -o graph_sfdp.png

graph_neato.png: graph.dot
	neato -Tpng graph.dot -o graph_neato.png

graph_twopi.png: graph.dot
	twopi -Tpng graph.dot -o graph_twopi.png

graph_osage.png: graph.dot
	osage -Tpng graph.dot -o graph_osage.png

graph_patchwork.png: graph.dot
	patchwork -Tpng graph.dot -o graph_patchwork.png

graph.dot: companies.csv graph_companies.py
	./graph_companies.py > graph.dot

clean:
	rm -rf graph*.png graph.dot
