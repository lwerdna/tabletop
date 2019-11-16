all: benelux.png benelux.svg

benelux.png: benelux.dot
	cat benelux.dot | dot -Tpng -o benelux.png

benelux.svg: benelux.dot
	cat benelux.dot | dot -Tsvg -o benelux.svg

