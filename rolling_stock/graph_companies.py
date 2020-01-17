#!/usr/bin/env python

import helpers
data = helpers.load_company_data()

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
