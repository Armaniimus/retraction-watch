import pandas as pd

def get_csv(source, index, array):
	df = pd.read_csv(source, index_col=index, usecols=array)
	return df

def get_chunked_csv(source, index, array, chunksize=100_000):
	df = pd.read_csv(source, index_col=index, usecols=array, chunksize=chunksize)
	return df

def save_csv(df, path):
	df.to_csv(path, index=True)

def count(df, colName):
	return df[colName].value_counts()

def add_none_column(df):
	return df.assign(None)

def print_dataframe(df, max=float('inf')):
	headline = ""
	if df.index.name == "":
		headline += "index"
	else:
		headline += f"{df.index.name}"

	for k in df.keys():
		headline += f", {k}"
		
	print(headline)


	index = 0
	for item in df.itertuples():
		if (max < index ):
			break
		line = ""
		for i in range(len(item)):
			if i == 0:
				line += f"{item[i]}"
			else:
				line += f", {item[i]}"
		index+= 1
		
		print(f"{line}")