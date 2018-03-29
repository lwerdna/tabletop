#!/bin/sh

# make canvas with cut guides
if [ ! -f "canvas.png" ]; then
	convert -size 2750x2125 xc:white canvas.png;
	# 377 comes from (2750 - (3*665))/2.0
	convert -draw "line 377,0 377,2125" canvas.png canvas.png
	convert -draw "line 1042,0 1042,2125" canvas.png canvas.png
	convert -draw "line 1707,0 1707,2125" canvas.png canvas.png
	convert -draw "line 2372,0 2372,2125" canvas.png canvas.png
	# 92 comes from (2125 - (2*970))/2.0
	convert -draw "line 0,92 2750,92" canvas.png canvas.png
	convert -draw "line 0,1063 2750,1063" canvas.png canvas.png
	convert -draw "line 0,2033 2750,2033" canvas.png canvas.png
fi

echo generating sheet 0...
cp canvas.png sheet0.png
convert -crop 665x970+78+78 ./cards/Ui5ZN3Y.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet0.png sheet0.png
convert -crop 665x970+78+78 ./cards/Jd9pKa8.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet0.png sheet0.png
convert -crop 665x970+78+78 ./cards/UcpkBaX.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet0.png sheet0.png
convert -crop 665x970+78+78 ./cards/mYSnRmN.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet0.png sheet0.png
convert -crop 665x970+78+78 ./cards/v5SLf5U.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet0.png sheet0.png
convert -crop 665x970+78+78 ./cards/VtC83bu.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet0.png sheet0.png

echo generating sheet 1...
cp canvas.png sheet1.png
convert -crop 665x970+78+78 ./cards/9dEOdMQ.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet1.png sheet1.png
convert -crop 665x970+78+78 ./cards/gIZFV49.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet1.png sheet1.png
convert -crop 665x970+78+78 ./cards/Vfk4duq.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet1.png sheet1.png
convert -crop 665x970+78+78 ./cards/exf7fSs.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet1.png sheet1.png
convert -crop 665x970+78+78 ./cards/oLlBUWl.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet1.png sheet1.png
convert -crop 665x970+78+78 ./cards/e4K8xnJ.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet1.png sheet1.png

echo generating sheet 2...
cp canvas.png sheet2.png
convert -crop 665x970+78+78 ./cards/7fzBsFG.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet2.png sheet2.png
convert -crop 665x970+78+78 ./cards/j1ZzBsL.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet2.png sheet2.png
convert -crop 665x970+78+78 ./cards/2oCZeOT.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet2.png sheet2.png
convert -crop 665x970+78+78 ./cards/dolrS90.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet2.png sheet2.png
convert -crop 665x970+78+78 ./cards/TPtiT33.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet2.png sheet2.png
convert -crop 665x970+78+78 ./cards/M9EIOoX.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet2.png sheet2.png

echo generating sheet 3...
cp canvas.png sheet3.png
convert -crop 665x970+78+78 ./cards/O6ZwShl.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet3.png sheet3.png
convert -crop 665x970+78+78 ./cards/EgWsgTT.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet3.png sheet3.png
convert -crop 665x970+78+78 ./cards/eKIVuvl.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet3.png sheet3.png
convert -crop 665x970+78+78 ./cards/z7v7gQl.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet3.png sheet3.png
convert -crop 665x970+78+78 ./cards/DhLrQ7D.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet3.png sheet3.png
convert -crop 665x970+78+78 ./cards/USUnkzh.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet3.png sheet3.png

echo generating sheet 4...
cp canvas.png sheet4.png
convert -crop 665x970+78+78 ./cards/zMlU9ws.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet4.png sheet4.png
convert -crop 665x970+78+78 ./cards/rc5Gipz.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet4.png sheet4.png
convert -crop 665x970+78+78 ./cards/lIg0E19.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet4.png sheet4.png
convert -crop 665x970+78+78 ./cards/0E7QQ4W.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet4.png sheet4.png
convert -crop 665x970+78+78 ./cards/0sSIuF4.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet4.png sheet4.png
convert -crop 665x970+78+78 ./cards/i82oKeh.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet4.png sheet4.png

echo generating sheet 5...
cp canvas.png sheet5.png
convert -crop 665x970+78+78 ./cards/pbdDf2x.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet5.png sheet5.png
convert -crop 665x970+78+78 ./cards/mT0sjWv.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet5.png sheet5.png
convert -crop 665x970+78+78 ./cards/OkH8CHY.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet5.png sheet5.png
convert -crop 665x970+78+78 ./cards/ybS9yhQ.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet5.png sheet5.png
convert -crop 665x970+78+78 ./cards/YsNrL56.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet5.png sheet5.png
convert -crop 665x970+78+78 ./cards/uvDUzRI.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet5.png sheet5.png

echo generating sheet 6...
cp canvas.png sheet6.png
convert -crop 665x970+78+78 ./cards/N00I7a1.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet6.png sheet6.png
convert -crop 665x970+78+78 ./cards/rPhkftC.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet6.png sheet6.png
convert -crop 665x970+78+78 ./cards/JEHbSNH.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet6.png sheet6.png
convert -crop 665x970+78+78 ./cards/hjVqd6e.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet6.png sheet6.png
convert -crop 665x970+78+78 ./cards/Xlc9eRB.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet6.png sheet6.png
convert -crop 665x970+78+78 ./cards/wQ2Yolf.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet6.png sheet6.png

echo generating sheet 7...
cp canvas.png sheet7.png
convert -crop 665x970+78+78 ./cards/K3xi0Lj.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet7.png sheet7.png
convert -crop 665x970+78+78 ./cards/ckR6Lwm.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet7.png sheet7.png
convert -crop 665x970+78+78 ./cards/y1a7WFu.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet7.png sheet7.png
convert -crop 665x970+78+78 ./cards/YljPwlw.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet7.png sheet7.png
convert -crop 665x970+78+78 ./cards/juycNBY.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet7.png sheet7.png
convert -crop 665x970+78+78 ./cards/TwIivJj.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet7.png sheet7.png

echo generating sheet 8...
cp canvas.png sheet8.png
convert -crop 665x970+78+78 ./cards/PSIblK0.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet8.png sheet8.png
convert -crop 665x970+78+78 ./cards/W4SljjG.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet8.png sheet8.png
convert -crop 665x970+78+78 ./cards/5BPZie6.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet8.png sheet8.png
convert -crop 665x970+78+78 ./cards/HwLr1Lr.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet8.png sheet8.png
convert -crop 665x970+78+78 ./cards/txnWRpW.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet8.png sheet8.png
convert -crop 665x970+78+78 ./cards/bXlVP9Z.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet8.png sheet8.png

echo generating sheet 9...
cp canvas.png sheet9.png
convert -crop 665x970+78+78 ./cards/L92KFNh.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet9.png sheet9.png
convert -crop 665x970+78+78 ./cards/ntEEl1J.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet9.png sheet9.png
convert -crop 665x970+78+78 ./cards/hPgygzB.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet9.png sheet9.png
convert -crop 665x970+78+78 ./cards/amGKBFJ.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet9.png sheet9.png
convert -crop 665x970+78+78 ./cards/Ci5BS4t.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet9.png sheet9.png
convert -crop 665x970+78+78 ./cards/mudObqd.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet9.png sheet9.png

echo generating sheet 10...
cp canvas.png sheet10.png
convert -crop 665x970+78+78 ./cards/YzHuR0d.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet10.png sheet10.png
convert -crop 665x970+78+78 ./cards/KuwusZV.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet10.png sheet10.png
convert -crop 665x970+78+78 ./cards/71m1w3i.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet10.png sheet10.png
convert -crop 665x970+78+78 ./cards/9RwVakv.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet10.png sheet10.png
convert -crop 665x970+78+78 ./cards/lzumrHX.png card.png
composite -gravity NorthWest -geometry +1042+1062 card.png sheet10.png sheet10.png
convert -crop 665x970+78+78 ./cards/lS8kMod.png card.png
composite -gravity NorthWest -geometry +1707+1062 card.png sheet10.png sheet10.png

echo generating sheet 11...
cp canvas.png sheet11.png
convert -crop 665x970+78+78 ./cards/F9WFzNv.png card.png
composite -gravity NorthWest -geometry +377+92 card.png sheet11.png sheet11.png
convert -crop 665x970+78+78 ./cards/TOr4YQV.png card.png
composite -gravity NorthWest -geometry +1042+92 card.png sheet11.png sheet11.png
convert -crop 665x970+78+78 ./cards/1IBnyun.png card.png
composite -gravity NorthWest -geometry +1707+92 card.png sheet11.png sheet11.png
convert -crop 665x970+78+78 ./cards/jknaDzA.png card.png
composite -gravity NorthWest -geometry +377+1062 card.png sheet11.png sheet11.png

