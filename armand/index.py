from genlib import *
from lib import *

def saveUniqueSubjects():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Title', 'Subject', 'Institution', 'Journal', 'Publisher', 'Country', 'Author', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ])
	data = get_unique_values(df, "Subject")
	save_csv(data, "data/subjects.csv")
	print_dataframe(data)

def saveUniqueCodes():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Title', 'Subject', 'Institution', 'Journal', 'Publisher', 'Country', 'Author', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ])
	data = get_unique_codes(df, "Subject")
	save_csv(data, "data/codes.csv")
	print_dataframe(data)

def save_days_inbetween():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'RetractionDate', 'OriginalPaperDate'], 100_000)
	data = add_counted_dates(df)
	save_csv(data, "data/dates.csv")

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

df = get_csv('data/source.csv', 'Record ID', ['Record ID', "Subject" ])
save_csv(df, "data/example.csv")