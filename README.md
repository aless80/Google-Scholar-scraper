# Google-Scholar-Scraper
Download information from Google Scholar for a number of author names. 

The main piece of information reported is the **h-index**, which is a commonly used metric for a scholar's importance:

*The h-index is an author-level metric that attempts to measure both the productivity and citation impact of the publications of a scientist or scholar.* [Wikipedia](https://en.wikipedia.org/wiki/H-index)


### Requirements
Installation of [Scholarly PyPI](https://pypi.org/project/scholarly/): 
```
pip3 install -U git+https://github.com/OrganicIrradiation/scholarly.git	
```

Install other common packages (pandas): 
```
pip install -r requirements.txt
```

### Usage:
	```
	python3 parse_scholarly.py --help
	python3 parse_scholarly.py <file-with-names>
	```

	where <file-with-names> is a file with a scholar on each row

### Output:
	* A print out authors and their h-index
	* A pickle file `data.pkl` with the collected raw data
	* A pickle file `data_flat.pkl` with a DataFrame containing the flattened data and no duplicates
	* An html file `names.html` showing a table with the flattened DataFrame above

### Notes:
	The script takes about 30s per author. That is due to [Scholarly](https://pypi.org/project/scholarly/)
	
