import pandas as pd
from sklearn import preprocessing

def allHotencoding(df:pd.DataFrame, singleHotEncodeColumns:list, multiHotEncodeColumns:list, split_char:str)-> pd.DataFrame:
	df = singleHotEncoding(df, singleHotEncodeColumns)
	return iterativeMultiHotEncoding(df, multiHotEncodeColumns, split_char)

def iterativeMultiHotEncoding(df:pd.DataFrame, col_names:list, split_char:str) -> pd.DataFrame:
	for name in col_names:
		df = multiHotEncoding(df, name, split_char)
	return df

def multiHotEncoding(df:pd.DataFrame, col_name:str, split_char:str) -> pd.DataFrame:
	mlb = preprocessing.MultiLabelBinarizer()
	cleaned_series = (
		df[col_name]
		.fillna('')
		.str.lower()
		.str.split(f'\\s*{split_char}\\s*')  # Regex handles ' ; ' and ';' the same
		.apply(lambda lst: [item for item in lst if item])  # Removes empty strings like ''
	)
	
	new_df = pd.DataFrame(
		mlb.fit_transform(cleaned_series),
		columns=mlb.classes_,
		index=df.index
	)
	new_df = new_df.add_prefix(f"{col_name}_")
	
	return pd.concat([df.drop(columns=[col_name]), new_df], axis=1)

def singleHotEncoding(df:pd.DataFrame, col_names: list) -> pd.DataFrame:
	return pd.get_dummies(df, columns=col_names, prefix=col_names, dummy_na=True)
