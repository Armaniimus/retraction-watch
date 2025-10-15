import pandas as pd
from pandas.api.types import is_string_dtype
import matplotlib.pyplot as plt
from sklearn import preprocessing

def get_csv(filepath:str, index:str|int, array:list=None) -> pd.DataFrame:
	if array == None:
		return pd.read_csv(filepath, index_col=index)
	return pd.read_csv(filepath, index_col=index, usecols=array)

def save_csv(df:pd.DataFrame, path:str) -> None:
	df.to_csv(path, index=True)

def count(df:pd.DataFrame, col_name:str) -> pd.DataFrame:
	df_out = df[col_name].dropna()
	
	if is_string_dtype(df[col_name]):
		df_out = df_out.str.strip()

	df_out = df_out.value_counts().to_frame().reset_index()
	
	df_out.index.name = "ID"
	df_out.columns = [col_name, 'count']
	return df_out

def split_and_count(df_in:pd.DataFrame, col_name:str, split_str:str=";") -> pd.DataFrame:
	if len(df_in) <= 0:	
		return count(df_in, col_name)
	
	temp_df = df_in[col_name].str.split(split_str, expand=True).stack()
	df_out = temp_df.str.strip().value_counts(dropna=True).to_frame().reset_index()
	df_out.columns = [col_name, 'count']
	df_out = df_out[df_out[col_name] != '']
	df_out.index.name = "ID"
	return df_out

def add_counted_dates(df:pd.DataFrame, start_date:str, end_date:str, new_col_name:str, format:str=None) -> pd.DataFrame:
	df = df.copy()
	#for format documentation see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
	df[start_date] = pd.to_datetime(df[start_date], format=format)
	df[end_date] = pd.to_datetime(df[end_date], format=format)
	df[new_col_name] = (df[end_date] - df[start_date]).dt.days

	return df

def print_dataframe(df:pd.DataFrame, max=float('inf')) -> None:
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

def visualize(df:pd.DataFrame, title:str, labels:str, data:str, path:str="") -> None:
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

def multiHotEncoding(df:pd.DataFrame, col_name:str, split_char:str) -> pd.DataFrame:
	#initiate the mlb instance
    mlb = preprocessing.MultiLabelBinarizer()
    
    #get the dataset from transformed column
    new_df = pd.DataFrame(mlb.fit_transform(df[col_name].str.strip(split_char).str.split(split_char)),
		columns=mlb.classes_,
		index=df.index
	)
    return pd.concat([df.drop(columns=[col_name]), new_df], axis=1)

def delete_empty_columns(df:pd.DataFrame):
	return df.loc[:, (df != 0).any(axis=0)]

def iterativeMultiHotEncoding(df:pd.DataFrame, col_names:list, split_char:str) -> pd.DataFrame:
	for name in col_names:
		df = multiHotEncoding(df, name, split_char)
	return df