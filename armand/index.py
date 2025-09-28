from genlib import *
from lib import *

def saveUniqueSubjects():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Title', 'Subject', 'Institution', 'Journal', 'Publisher', 'Country', 'Author', 'ArticleType', 'RetractionDate', 'OriginalPaperDate', 'RetractionNature', 'Reason', 'Paywalled' ])
	data = get_unique_values(df, "Subject")
	save_csv(data, "data/subjects.csv")
	print_dataframe(data)

def save_days_inbetween():
	df = get_chunked_csv('data/source.csv', 'Record ID', ['Record ID', 'RetractionDate', 'OriginalPaperDate'], 100_000)
	data = add_counted_dates(df)
	save_csv(data, "data/dates.csv")

def visualize_general(collumn, in2022, cutPercentage):
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', collumn, 'OriginalPaperDate' ])
	if in2022:
		df2022 = cutNot2022(df)
		title = f'Distribution of {collumn}s outside of 2022'
		path = f"figures/{collumn}s-not2022.png"
	else:
		df2022 = cut2022(df)
		title = f'Distribution of {collumn}s in 2022'
		path = f"figures/{collumn}s-2022.png"
	data = get_unique_values(df2022, collumn)

	data = combine_into_others(data, cutPercentage, collumn)
	visualize(data, title, collumn, 'count', path)
	

# save_days_inbetween()
saveUniqueSubjects()
# subjectsIn2022()

# visualize_general("Subject", True, 1.5)
# visualize_general("Subject", False, 1.5)

# visualize_general("Country", True, 1)
# visualize_general("Country", False, 1)

# visualize_general("Reason", True, 1)
# visualize_general("Reason", False, 1)