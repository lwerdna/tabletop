#!/usr/bin/env python

# this generates the make_card_sheets.sh script
# ./generate.py > make_card_sheets.sh

print '#!/bin/sh'
print ''
print '# make canvas with cut guides'
print 'if [ ! -f "canvas.png" ]; then'
print '	convert -size 2750x2125 xc:white canvas.png;'
print '	# 377 comes from (2750 - (3*665))/2.0'
print '	convert -draw "line 377,0 377,2125" canvas.png canvas.png'
print '	convert -draw "line 1042,0 1042,2125" canvas.png canvas.png'
print '	convert -draw "line 1707,0 1707,2125" canvas.png canvas.png'
print '	convert -draw "line 2372,0 2372,2125" canvas.png canvas.png'
print '	# 92 comes from (2125 - (2*970))/2.0'
print '	convert -draw "line 0,92 2750,92" canvas.png canvas.png'
print '	convert -draw "line 0,1063 2750,1063" canvas.png canvas.png'
print '	convert -draw "line 0,2033 2750,2033" canvas.png canvas.png'
print 'fi'

print ''

files = [ 'Ui5ZN3Y.png', 'Jd9pKa8.png', 'UcpkBaX.png', 'mYSnRmN.png', 'v5SLf5U.png', 'VtC83bu.png', '9dEOdMQ.png', 'gIZFV49.png', 'Vfk4duq.png', 'exf7fSs.png', 'oLlBUWl.png', 'e4K8xnJ.png', '7fzBsFG.png', 'j1ZzBsL.png', '2oCZeOT.png', 'dolrS90.png', 'TPtiT33.png', 'M9EIOoX.png', 'O6ZwShl.png', 'EgWsgTT.png', 'eKIVuvl.png', 'z7v7gQl.png', 'DhLrQ7D.png', 'USUnkzh.png', 'zMlU9ws.png', 'rc5Gipz.png', 'lIg0E19.png', '0E7QQ4W.png', '0sSIuF4.png', 'i82oKeh.png', 'pbdDf2x.png', 'mT0sjWv.png', 'OkH8CHY.png', 'ybS9yhQ.png', 'YsNrL56.png', 'uvDUzRI.png', 'N00I7a1.png', 'rPhkftC.png', 'JEHbSNH.png', 'hjVqd6e.png', 'Xlc9eRB.png', 'wQ2Yolf.png', 'K3xi0Lj.png', 'ckR6Lwm.png', 'y1a7WFu.png', 'YljPwlw.png', 'juycNBY.png', 'TwIivJj.png', 'PSIblK0.png', 'W4SljjG.png', '5BPZie6.png', 'HwLr1Lr.png', 'txnWRpW.png', 'bXlVP9Z.png', 'L92KFNh.png', 'ntEEl1J.png', 'hPgygzB.png', 'amGKBFJ.png', 'Ci5BS4t.png', 'mudObqd.png', 'YzHuR0d.png', 'KuwusZV.png', '71m1w3i.png', '9RwVakv.png', 'lzumrHX.png', 'lS8kMod.png', 'F9WFzNv.png', 'TOr4YQV.png', '1IBnyun.png', 'jknaDzA.png' ]

sheet = 0

positions = ['+377+92', '+1042+92', '+1707+92', '+377+1062', '+1042+1062', '+1707+1062']

while files:
	group = files[0:6]

	print "echo generating sheet %d..." % sheet
	print 'cp canvas.png sheet%d.png' % sheet

	for (i,fname) in enumerate(group):
		print 'convert -crop 665x970+78+78 ./cards/%s card.png' % fname
		print 'composite -gravity NorthWest -geometry %s card.png sheet%d.png sheet%d.png' % (positions[i], sheet, sheet)

	print ''

	files = files[6:]
	sheet += 1
	
