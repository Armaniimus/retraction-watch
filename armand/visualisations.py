from genlib import *
from lib import *

def subjectsIn2022():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Subject', 'OriginalPaperDate' ])
	df2022 = cut2022(df)
	
	data = get_unique_values(df2022, "Subject")
	save_csv(data, "data/subjectsIn2022.csv")
	print_dataframe(data)

def visualizeSubjects():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Subject', 'OriginalPaperDate' ])
	df2022 = cut2022(df)
	
	data = get_unique_values(df2022, "Subject")
	data = combine_into_others(data, 1.5, "Subject")
	visualize(data, 'Distribution of Subjects in 2022', 'Subject', 'count', "figures/subjects-2022.png")

def visualizeSubjectsNot2022():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Subject', 'OriginalPaperDate' ])
	df2022 = cutNot2022(df)
	
	data = get_unique_values(df2022, "Subject")
	data = combine_into_others(data, 1.5, "Subject")
	visualize(data, 'Distribution of Subjects not in 2022', 'Subject', 'count', "figures/subjects-not2022.png")

def visualize_countries():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Country', 'OriginalPaperDate' ])
	df2022 = cut2022(df)
	data = get_unique_values(df2022, "Country")
	
	data = combine_into_others(data, 1, "Country")
	visualize(data, 'Distribution of countries in 2022', 'Country', 'count', "figures/countries-2022.png")

def visualize_countries_Not2022():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Country', 'OriginalPaperDate' ])
	df2022 = cutNot2022(df)
	data = get_unique_values(df2022, "Country")

	data = combine_into_others(data, 1, "Country")
	visualize(data, 'Distribution of countries outside of 2022', 'Country', 'count', "figures/countries-not2022.png")

def visualize_reasons():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Reason', 'OriginalPaperDate' ])
	df2022 = cut2022(df)
	data = get_unique_values(df2022, 'Reason')

	data = combine_into_others(data, 1, "Reason")
	visualize(data, 'Distribution of reasons in 2022', 'Reason', 'count', "figures/reasons-2022.png")

def visualize_reasons_Not2022():
	df = get_csv('data/source.csv', 'Record ID', ['Record ID', 'Reason', 'OriginalPaperDate' ])
	df2022 = cutNot2022(df)
	data = get_unique_values(df2022, 'Reason')

	data = combine_into_others(data, 1, "Reason")
	visualize(data, 'Distribution of reasons outside of 2022', 'Reason', 'count', "figures/reasons-not2022.png")

# visualizeSubjects()
# visualizeSubjectsNot2022()

# visualize_countries()
# visualize_countries_Not2022()

# visualize_reasons()
# visualize_reasons_Not2022()