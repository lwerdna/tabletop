#!/usr/bin/env python

import helpers

def color2html(color):
	if color == 'blue': color='lightblue'
	if color == 'green': color='lightgreen'
	if color == 'purple': color='mediumpurple'
	return color

def arr2d_to_html(arr, headings=None):
	print('<table border=1 cellspacing=0>')

	if headings:
		print('<tr>')
		for h in headings:
			print('<th>%s</th>' % h)
		print('</tr>')

	for row in arr:
		print('<tr>')
		for col in row:
			if col == None:
				print('\t<td></td>')
			else:
				print('\t<td>%s</td>' % col)
		print('</tr>')
	print('</table>')

# 
palette = [
'#FFFFCC','#FFFECA','#FFFDC9','#FFFDC7','#FFFCC6','#FFFCC5','#FFFBC3','#FFFBC2',
'#FFFAC0','#FFF9BF','#FFF9BE','#FFF8BC','#FFF8BB','#FFF7BA','#FFF7B8','#FFF6B7',
'#FFF5B5','#FFF5B4','#FFF4B3','#FFF4B1','#FFF3B0','#FFF3AF','#FFF2AD','#FFF2AC',
'#FFF1AA','#FFF0A9','#FFF0A8','#FFEFA6','#FFEFA5','#FFEEA3','#FFEEA2','#FFEDA1',
'#FEEC9F','#FEEC9E','#FEEB9D','#FEEB9B','#FEEA9A','#FEE999','#FEE997','#FEE896',
'#FEE795','#FEE793','#FEE692','#FEE691','#FEE590','#FEE48E','#FEE48D','#FEE38C',
'#FEE28A','#FEE289','#FEE188','#FEE186','#FEE085','#FEDF84','#FEDF82','#FEDE81',
'#FEDD80','#FEDD7E','#FEDC7D','#FEDB7C','#FEDB7A','#FEDA79','#FEDA78','#FED976',
'#FED875','#FED774','#FED673','#FED571','#FED370','#FED26F','#FED16D','#FED06C',
'#FECE6B','#FECD69','#FECC68','#FECB67','#FECA65','#FEC864','#FEC763','#FEC661',
'#FEC560','#FEC35F','#FEC25D','#FEC15C','#FEC05B','#FEBF5A','#FEBD58','#FEBC57',
'#FEBB56','#FEBA54','#FEB853','#FEB752','#FEB650','#FEB54F','#FEB34E','#FEB24C',
'#FDB14B','#FDB04B','#FDAF4A','#FDAE4A','#FDAC49','#FDAB49','#FDAA48','#FDA948',
'#FDA847','#FDA747','#FDA546','#FDA446','#FDA345','#FDA245','#FDA144','#FDA044',
'#FD9E43','#FD9D43','#FD9C42','#FD9B42','#FD9A41','#FD9941','#FD9840','#FD9640',
'#FD953F','#FD943F','#FD933E','#FD923E','#FD913D','#FD8F3D','#FD8E3C','#FD8D3C',
'#FC8C3B','#FC8A3B','#FC883A','#FC863A','#FC8439','#FC8238','#FC8038','#FC7E37',
'#FC7C37','#FC7A36','#FC7836','#FC7635','#FC7434','#FC7234','#FC7033','#FC6E33',
'#FC6C32','#FC6A32','#FC6831','#FC6630','#FC6430','#FC622F','#FC602F','#FC5E2E',
'#FC5C2E','#FC5A2D','#FC582D','#FC562C','#FC542B','#FC522B','#FC502A','#FC4E2A',
'#FB4C29','#FA4B29','#F94928','#F94828','#F84627','#F74427','#F64327','#F64126',
'#F53F26','#F43E25','#F33C25','#F23B24','#F23924','#F13724','#F03623','#EF3423',
'#EE3222','#EE3122','#ED2F21','#EC2D21','#EB2C20','#EB2A20','#EA2920','#E9271F',
'#E8251F','#E7241E','#E7221E','#E6201D','#E51F1D','#E41D1C','#E31C1C','#E31A1C',
'#E2191C','#E0181C','#DF171C','#DE161D','#DD161D','#DC151D','#DA141E','#D9131E',
'#D8121E','#D7121F','#D6111F','#D4101F','#D30F20','#D20E20','#D10D20','#D00D20',
'#CF0C21','#CD0B21','#CC0A21','#CB0922','#CA0922','#C90822','#C70723','#C60623',
'#C50523','#C40424','#C30424','#C10324','#C00225','#BF0125','#BE0025','#BD0025',
'#BB0026','#B90026','#B70026','#B50026','#B30026','#B10026','#AF0026','#AD0026',
'#AC0026','#AA0026','#A80026','#A60026','#A40026','#A20026','#A00026','#9E0026',
'#9C0026','#9A0026','#980026','#960026','#950026','#930026','#910026','#8F0026',
'#8D0026','#8B0026','#890026','#870026','#850026','#830026','#810026','#800026']
assert len(palette) == 256

companies = helpers.load_company_data()

yields = [companies[x]['income']/companies[x]['facevalue']*100.0 for x in companies]
yield_min = min(yields)
yield_range = 50 - yield_min

margins = [100*(companies[x]['max'] - companies[x]['facevalue']) / companies[x]['facevalue'] for x in companies]
margin_min = min(margins)
margin_range = 50 - margin_min

headers = ['ticker','face value', 'price', 'income', 'yield', 'margin', 'synergies']
arr = []
for ticker in sorted(companies.keys(), key=lambda x:companies[x]['facevalue']):
	data = companies[ticker]
	row = []
	row.append('<span style="background-color:%s">%s</span>' % (color2html(data['color']), ticker))
	row.append(data['facevalue'])
	row.append('[%d, %d]' % (data['min'], data['max']))
	row.append('%d' % data['income'])
	yield_ = (data['income']/data['facevalue'])*100
	if yield_ >= 50:
		yield_color = palette[-1]
	else:
		yield_color = palette[int(255 * (yield_-15)/35)]
	row.append('<span style="background-color:%s">%.02f%%</span>' % (yield_color, yield_))
	# margin
	margin = 100*(data['max'] - data['facevalue'])/data['facevalue']
	if margin >= 50:
		margin_color = palette[-1]
	else:
		margin_color = palette[int(255 * (margin-15)/35)]
	row.append('%d (<span style="background-color:%s">%.02f%%</span>)' % (data['max'] - data['facevalue'], margin_color, margin))

	#synstr = '%d:' % len(data['synergies'])
	synstr = ''
	for (syncomp, synamt) in data['synergies'].items():
		synstr += ' %s+%d' % (syncomp, synamt)
	row.append(synstr)
	# row done
	arr.append(row)
arr2d_to_html(arr, headers)
