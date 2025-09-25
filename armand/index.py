from genlib import *
from lib import *

def saveUniqueSubjects():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Title', 'Subject', 'Institution', 'Journal', 'Publisher', 'Country', 'Author', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ])
	data = get_unique_subjects(df)
	save_csv(data, "data/subjects.csv")
	print_dataframe(data)

def save_days_inbetween():
	df = get_chunked_csv('data/source.csv', 'Record ID', ['Record ID', 'RetractionDate', 'OriginalPaperDate'], 100_000)
	data = add_counted_dates(df)
	save_csv(data, "data/dates.csv")

# save_days_inbetween()
# saveUniqueSubjects()
