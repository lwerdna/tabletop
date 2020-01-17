#!/usr/bin/env python

data = {}
with open('companies.csv') as fp:
	for line in fp.readlines():
		line = line.strip()
		if not line or line.startswith('#'):
			continue
		(company,color,facevalue,min_,max_,income,synergies) = line.split(',')

		syndict = {}
		for comp_plus_bonus in synergies.split(' '):
			(comp_d, bonus) = comp_plus_bonus.split('+')
			syndict[comp_d] = int(bonus)

		data[company] = {	'color': color,
							'facevalue': int(facevalue),
							'min': int(min_),
							'max': int(max_),
							'income': int(income),
							'synergies': syndict	}

print('graph foo {')

for (company, stuff) in data.items():
	print('\t%s [label="%s" fillcolor="%s" style=filled];' % (company, company, stuff['color']))

seen = set()
for (company, stuff) in data.items():
	for syn in stuff['synergies'].keys():
		ident = '%s-%s' % tuple(sorted([company, syn]))
		if ident in seen:
			continue

		seen.add(ident)
		print('\t%s -- %s;' % (company, syn))
print('}')
