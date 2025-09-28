import pandas as pd
import matplotlib.pyplot as plt

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

def count_total_values(df, colName):
	return df[colName].nunique()

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

def visualize(df, title, index, count, path=""):
	df.set_index(index, inplace=True)
	df.sort_values(by=count, ascending=True)
	plt.figure(figsize=(16, 16))
	df[count].plot.pie(
		autopct="%1.1f%%",      # show percentages
		startangle=180,         # rotate start angle
		ylabel="",              # remove y-axis label
		legend=False
	)
	plt.title(title)

	if path != "":
		plt.savefig(path, bbox_inches='tight')
	else:
		plt.show()

def combine_into_others(df, split_percentage, index):
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