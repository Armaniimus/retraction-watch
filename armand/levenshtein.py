from genlib import get_unique_values
import pandas as pd
from Levenshtein import distance

def calc_distance(str1:str, str2:str)->int:
	return distance(str1, str2)

def levenstein_distance_column(df:pd.DataFrame, col_name:str, distance_limit:int=3):
	out = {}
	names_df = get_unique_values(df, col_name)
	df_sorted = names_df.sort_values(by='count', ascending=False).reset_index(drop=True)
	df_sorted2 = df_sorted.copy()

	index = 0
	for item in df_sorted.itertuples():
		df_sorted2.drop(index, inplace=True)
		att = getattr(item, col_name)
		
		for item2 in df_sorted2.itertuples():
			att2 = getattr(item2, col_name)

			dist = distance(att, att2)
			if dist <= distance_limit:
				if dist not in out:
					out[dist] = []
				out[dist].append(f"{att} -> {att2}")
		index+=1
	return out

def levenstein_distance_dataframe(df:pd.DataFrame, distance_limit:int=3):
	out = {}

	col_names = df.columns
	for c_name in col_names:
		out[c_name] = levenstein_distance_column(df, c_name, distance_limit=distance_limit)

	return out
	
			
def to_string_levenstein_distance_column(levenstein:dict)->str:
	out = ""

	for key in levenstein:
		out += f"distance[{key}]\n"
		for item in levenstein[key]:
			out += f"\t{item}\n"
		out += "\n"
	return out

def to_string_levenstein_distance_dataframe(levenstein:dict)->str:
	out = ""

	for column_key in levenstein:
		out += f"{column_key}\n"

		column = levenstein[column_key]
		for distance in column:
			out += f"\tdistance[{distance}]\n"
			for item in column[distance]:
				out += f"\t\t{item}\n"
			out += "\n"
		out += "\n"
	return out