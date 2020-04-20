#!/usr/bin/env python3

def load_company_data():
	result = {}

	with open('companies.csv') as fp:
		for line in fp.readlines():

			# company,color,facevalue,min,max,income,synergies
			#BME,red,1,1,2,1,KME+1 BD+1 HE+1 PR+1
			#BSE,red,2,1,3,1,BPM+1 SX+1 MS+1 PR+1
			#KME,red,5,3,7,2,BME+1 MHE+1 OL+1 HE+1 PR+1
			#AKE,red,6,3,8,2,BPM+1 MHE+1 OL+1 MS+1 PR+1
			# ...

			if line.startswith('#'):
				continue

			(company, color, facevalue, min_, max_, income, synergies) = line.split(',')
			result[company] = {'color':color, 'facevalue':int(facevalue), \
				'min':int(min_), 'max':int(max_), 'income':int(income)}

			result[company]['synergies'] = {}
			for ticker_amount in synergies.split(' '):
				(ticker, amount) = ticker_amount.split('+')
				result[company]['synergies'][ticker] = int(amount)

	return result


