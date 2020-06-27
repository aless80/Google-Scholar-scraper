#!/usr/bin/env python3
import sys
import pickle
from scholarly import scholarly
import time

doc_string = """
Usage:
	python3 parse_scholarly.py --help
	python3 parse_scholarly.py <file-with-names>

	where <file-with-names> is a file with a scholar on each row
Output:
	Print out authors and their h-index
	A pickle file `names.pkl` with the collected data
	An html file `names.html` showing a table with the collected data
Notes:
	For the library Scholarly refer to https://pypi.org/project/scholarly/
	Installation of Scholarly: 
	pip3 install -U git+https://github.com/OrganicIrradiation/scholarly.git	
	Scholarly takes about 30s per author

"""

# Print help
if len(sys.argv) < 2 or sys.argv[1] == '--help':
	print(doc_string)
	sys.exit()

# Parse the author names
file_in = sys.argv[1]
authornames = []
with open(file_in,'r') as f:
	for line in f:
		line = line.split('\n')[0]
		authornames.append(line)

# Indicate what data to get (see Author class in https://pypi.org/project/scholarly/)
sections = ['basics','indices']
max_homonyms = 5

#pip install free-proxy
from fp.fp import FreeProxy
proxy = FreeProxy(rand=True, timeout=1, country_id=['NO']).get()  
scholarly.use_proxy(http=proxy, https=proxy)


# Loop through the authors
t0 = time.time()
data = list({})
for i,authname in enumerate(authornames):
	hindices = []
	emails, names, affiliations, citedbys = [], [], [], []
	try:
		search_query = scholarly.search_author(authname)
		for _ in range(max_homonyms):
			try:
				author = next(search_query)
				tmp_data = author.fill(sections=sections)
				hindices.append(tmp_data.hindex)
				emails.append(tmp_data.email)
				names.append(tmp_data.name)
				affiliations.append(tmp_data.affiliation)
				citedbys.append(tmp_data.citedby)
			except:
				#Break inner loop on matching authors
				break
			data.append({'authorname':authname, 'hindices':hindices,
				'emails':emails, 'names':names, 'affiliations':affiliations, 'citedbys':citedbys})
	except:
		print('Author not found: %s' % authname)
		data.append({'authorname':authname, 'hindices':-1,
			'emails':-1, 'names':-1, 'affiliations':-1, 'citedby':-1})

	# Print out
	if len(hindices) == max_homonyms:
		print('Showing the first 10 matches found for author: %s' % authname)
	if len(hindices) > 1:
		print('%d matches found for author: %s' % \
			(len(hindices), authname))
	for hind in data[i]['hindices']:
		print('%s h-index=%d' %(data[i]['authorname'], hind))

print('%d authors completed in %ds' %(i, int(time.time()-t0)))

# Save to pkl
file_pkl = 'names.pkl'
with open(file_pkl, 'wb') as f:
	pickle.dump(data, f)
# Read it in with:
#import pickle
#file_pkl = 'names.pkl'
#with open(file_pkl, 'rb') as f: data = pickle.load(f)

# Write to a DataFrame, flatten it and remove duplicates
import pandas as pd
df = pd.DataFrame(data)

df_flat = pd.DataFrame({
	'authorname':df.authorname.repeat(df.citedbys.str.len()),
	'hindex':df.hindices.sum(),
	'name':df.names.sum(),
	'email':df.emails.sum(),
	'citedby':df.citedbys.sum(),
	'affiliation':df.affiliations.sum(),
	})
df_flat = df_flat.drop_duplicates()
df_flat.to_html('names.html')