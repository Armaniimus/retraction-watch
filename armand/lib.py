import pandas as pd
from genlib import visualize, get_csv

def get_opinionated_csv():
	return get_csv('data/source.csv', 'Record ID', ['Record ID', 'Title', 'Subject', 'Institution', 'Journal', 'Publisher', 'Country', 'Author', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ])

def add_counted_dates(df:pd.DataFrame):
	df['OriginalPaperDate'] = pd.to_datetime(df['OriginalPaperDate'])
	df['RetractionDate'] = pd.to_datetime(df['RetractionDate'])
	df['days_between'] = (df['RetractionDate'] - df['OriginalPaperDate']).dt.days

	return df

def get_unique_values(df_in:pd.DataFrame, col_name:str):
	unique_values = {}
	
	df = df_in[[col_name]].copy()
	for row in df.itertuples():
		splitfield = getattr(row, col_name).split(';')
		for s in splitfield:
			if s in unique_values.keys():
				unique_values[s] += 1
			elif s != '':
				unique_values[s] = 1		

	out = {
		"count": [],
		col_name: []
	}
	index = []

	id = 0
	for key in unique_values.keys():
		index.append(id)
		out["count"].append(unique_values[key])
		out[col_name].append(key)
		id += 1
	out = pd.DataFrame(out, index=index)
	out.index.name = "ID"
	return out

def get_unique_codes(dfIn:pd.DataFrame, col_name:str):
	df = get_unique_values(dfIn, col_name)

	unique_values = {}
	for row in df.itertuples():
		field = getattr(row, col_name)
		count = getattr(row, "count")
		code = field[field.find('(') + 1:field.find(')')]
		
		if code in unique_values.keys():
			unique_values[code] += count
		elif code != '':
			unique_values[code] = count	

	out = {
		"count": [],
		"code": []
	}
	index = []

	id = 0
	for key in unique_values.keys():
		index.append(id)
		out["count"].append(unique_values[key])
		out["code"].append(key)
		id += 1
	out = pd.DataFrame(out, index=index)
	out.index.name = "ID"
	return out

def combine_into_others(df:pd.DataFrame, split_percentage:int|float, index:str):
	total = df["count"].sum()

	# Calculate percentage
	df["percent"] = df["count"] / total * 100

	# Split into two groups: >=1% and <1%
	main_df = df[df["percent"] >= split_percentage].copy()
	others_df = df[df["percent"] < split_percentage].copy()

	# Combine the small ones into a single "Others" row
	others_sum = others_df["count"].sum()
	if others_sum > 0:
		main_df = pd.concat([
			main_df,
			pd.DataFrame({index: ["Others"], "count": [others_sum]})
		], ignore_index=True)

	# Sort again if needed
	return main_df.sort_values(by="count", ascending=False).reset_index(drop=True)

def cut2022(df:pd.DataFrame):
	# Convert 'published' column to datetime
	df["OriginalPaperDate"] = pd.to_datetime(df['OriginalPaperDate'], errors='coerce')

	# Filter rows where year == 2022
	return df[df["OriginalPaperDate"].dt.year == 2022]

def cutNot2022(df:pd.DataFrame):
	# Convert 'published' column to datetime
	df["OriginalPaperDate"] = pd.to_datetime(df['OriginalPaperDate'], errors='coerce')

	# Filter rows where year == 2022
	return df[df["OriginalPaperDate"].dt.year != 2022]

def visualize_general(collumn:str, in2022:bool, cut_percentage:int|float):
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', collumn, 'OriginalPaperDate' ])
	if in2022:
		df2022 = cutNot2022(df)
		title = f'Distribution of {collumn}s outside of 2022'
		path = f"figures/{collumn}s-not2022.png"
	else:
		df2022 = cut2022(df)
		title = f'Distribution of {collumn}s in 2022'
		path = f"figures/{collumn}s-2022.png"
	data = get_unique_values(df2022, collumn)

	data = combine_into_others(data, cut_percentage, collumn)
	visualize(data, title, collumn, 'count', path)
	
def visualize_codes(in2022:bool, cut_percentage:int|float):
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', "Subject", 'OriginalPaperDate' ])
	if in2022:
		df2022 = cutNot2022(df)
		title = f'Distribution of codes outside of 2022'
		path = f"figures/codes-not2022.png"
	else:
		df2022 = cut2022(df)
		title = f'Distribution of codes in 2022'
		path = f"figures/codes-2022.png"
	data = get_unique_codes(df2022, "Subject")

	data = combine_into_others(data, cut_percentage, "code")
	visualize(data, title, "code", 'count', path)