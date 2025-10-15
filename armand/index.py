from levenshtein import *
from genlib import *
from lib import *

def saveUniqueSubjects():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Title', 'Subject', 'Institution', 'Journal', 'Publisher', 'Country', 'Author', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ])
	data = split_and_count(df, "Subject")
	save_csv(data, "data/subjects.csv")
	print_dataframe(data)

def saveUniqueCodes():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Title', 'Subject', 'Institution', 'Journal', 'Publisher', 'Country', 'Author', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ])
	data = get_unique_codes(df, "Subject")
	save_csv(data, "data/codes.csv")
	print_dataframe(data)

def save_days_inbetween():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'RetractionDate', 'OriginalPaperDate'])
	data = context_aware_add_counted_dates(df, "days_between") 
	save_csv(data, "data/dates.csv")
	print(data)

def encode_data():
	df = get_opinionated_csv()
	in2022 = cut2022(df)
	data = context_aware_add_counted_dates(in2022, "days_in_between")
	multi_encoded_df = iterativeMultiHotEncoding(data, ["Subject", "Reason", "Country", "ArticleType"], ";")
	filteredDataframes = delete_empty_columns(multi_encoded_df)
	
	print(filteredDataframes)
	save_csv(filteredDataframes, "data/multiEncodingFiltered.csv")

# save_days_inbetween()

# save_days_inbetween()
# saveUniqueSubjects()
# saveUniqueCodes()
# subjectsIn2022()

# visualize_general("Subject", True, 1.5)
# visualize_general("Subject", False, 1.5)

# visualize_general("Country", True, 1)
# visualize_general("Country", False, 1)

# visualize_general("Reason", True, 1)
# visualize_general("Reason", False, 1)
# visualize_codes(True, 1)
# visualize_codes(False, 1)

# df = get_csv('data/source.csv', 'Record ID', ['Record ID', "Subject" ])
# save_csv(df, "data/example.csv")

# df = get_opinionated_csv()
# multi_encoded_df = multiHotEncoding(df, "Subject", ";")
# print(multi_encoded_df)
# save_csv(multi_encoded_df, "data/multiEncoding.csv")

# encode_data()

# print(calc_distance("ab","ac"))
# df = get_opinionated_csv()
# dic = levenstein_distance_column(df, "Subject")
# out = to_string_levenstein_distance_column(dic)
# print(out)

# df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Subject'])

df = get_opinionated_csv()
journal_df = count(df, "Journal")
print(journal_df)
save_csv(journal_df, "data/journal.csv")

# df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Subject', 'Country', 'ArticleType', 'Reason' ])
# dic = levenstein_distance_dataframe(df)
# out = to_string_levenstein_distance_dataframe(dic)
# print(out)
