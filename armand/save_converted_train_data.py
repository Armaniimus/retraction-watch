from genlib import save_csv
from hotEncoding import *
from lib import get_opinionated_csv, addIn2022, context_aware_add_counted_dates

def save_data():
	df = get_opinionated_csv()
	df = df[['Subject', 'Country', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ]]
	data = context_aware_add_counted_dates(df, "days_in_between")

	train_set = allHotencoding(data, ['RetractionNature', 'Paywalled'], ["Subject", "Reason", "Country", "ArticleType"], ";")
	train_set = addIn2022(train_set)
      
	train_set['RetractionDate'] = robust_date_to_timestamp(train_set['RetractionDate'])
	train_set['OriginalPaperDate'] = robust_date_to_timestamp(train_set['OriginalPaperDate'])
	target_set = train_set["in2022"]

	save_csv(train_set,  "data/train_set.csv")
	save_csv(target_set, "data/target_set.csv")

def robust_date_to_timestamp(series: pd.Series) -> pd.Series:
    # ... (the function we developed in the previous step) ...
    numeric_series = pd.to_numeric(series, errors='coerce')
    is_date_string = numeric_series.isna()
    datetime_converted = (pd.to_datetime(series.loc[is_date_string]).astype('int64') // 10**9)
    final_series = numeric_series.fillna(datetime_converted)
    return final_series.astype('int64')

save_data()