from genlib import *
from lib import *

def saveUniqueSubjects():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Title', 'Subject', 'Institution', 'Journal', 'Publisher', 'Country', 'Author', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ])
	data = get_unique_subjects(df)
	save_csv(data, "data/subjects.csv")
	print_dataframe(data)

def save_days_inbetween():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'RetractionDate', 'OriginalPaperDate'])
	data = add_counted_dates(df)
	save_csv(data, "data/dates.csv")
	print_dataframe(data, 100)

save_days_inbetween()