#!/usr/bin/env python

def findall(data, pattern=b'\x89PNG\x0d\x0a'):
    i = data.find(pattern)
    while i != -1:
        yield i
        i = data.find(pattern, i+1)

with open('resources.mp3', 'rb') as fp:
	data = fp.read()

locs = list(findall(data))

for (i,start) in enumerate(locs):
	if i<len(locs)-1:
		subdata = data[start:locs[i+1]]
	else:
		subdata = data[start:]

	with open('extract_0x%X.png'%start,'wb') as fp:
		fp.write(subdata)

