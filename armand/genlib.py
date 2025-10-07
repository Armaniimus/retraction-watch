import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

def get_csv(filepath:str, index:str|int, array:list=None):
	if array == None:
		return pd.read_csv(filepath, index_col=index)
	return pd.read_csv(filepath, index_col=index, usecols=array)

def save_csv(df:pd.DataFrame, path:str):
	df.to_csv(path, index=True)

def count(df:pd.DataFrame, col_name:str):
	return df[col_name].value_counts()

def count_total_values(df:pd.DataFrame, col_name:str):
	return df[col_name].nunique()

def add_none_column(df:pd.DataFrame):
	return df.assign(None)

def print_dataframe(df:pd.DataFrame, max=float('inf')):
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

def visualize(df:pd.DataFrame, title:str, labels:str, data:str, path:str=""):
	df.set_index(labels, inplace=True)
	df.sort_values(by=data, ascending=True)
	plt.figure(figsize=(10, 10))
	df[data].plot.pie(
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

def multiHotEncoding(df:pd.DataFrame, col_name:str, split_char:str):
	#initiate the mlb instance
    mlb = preprocessing.MultiLabelBinarizer()
    
    #get the dataset from transformed column
    new_df = pd.DataFrame(mlb.fit_transform(df[col_name].str.split(split_char)),
		columns=mlb.classes_,
		index=df.index
	)
    return pd.concat([df.drop(columns=col_name),new_df],axis=1)

def iterativeMultiHotEncoding(df:pd.DataFrame, col_names:list, split_char:str):
	for name in col_names:
		df = multiHotEncoding(df, name, split_char)
	return df
