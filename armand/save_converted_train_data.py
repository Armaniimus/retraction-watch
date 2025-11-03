from libs.cleaning.genlib import save_csv
from libs.cleaning.hotEncoding import *
from libs.cleaning.lib import get_opinionated_csv, addIn2022, context_aware_add_counted_dates

def save_data():
	df = get_opinionated_csv()
	df = df[['Subject', 'Country', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ]]
	data = context_aware_add_counted_dates(df, "days_in_between")

	train_set= allHotencoding(data, ['RetractionNature', 'Paywalled'], ["Subject", "Reason", "Country", "ArticleType"], ";")
	train_set = addIn2022(train_set.copy())
      
	train_set['OriginalPaperDate'] = robust_date_to_timestamp(train_set['OriginalPaperDate'])
	train_set = train_set[train_set['OriginalPaperDate'] >= 0]
	target_set = train_set["in2022"]
	train_set = train_set.drop(columns=['RetractionDate', 'in2022']) 
	
	train_set.to_csv("data/train_set.csv", index=False)
	target_set.to_csv("data/target_set.csv", index=False)

def robust_date_to_timestamp(series: pd.Series) -> pd.Series:
    numeric_series = pd.to_numeric(series, errors='coerce')
    is_date_string = numeric_series.isna()
    datetime_converted = (pd.to_datetime(series.loc[is_date_string]).astype('int64') // 10**9)
    final_series = numeric_series.fillna(datetime_converted)
    return final_series.astype('int64')

save_data()