import pandas as pd

def add_counted_dates(df):
	processed_chunks = []
	for chunk in df:
		chunk['OriginalPaperDate'] = pd.to_datetime(chunk['OriginalPaperDate'], errors='coerce')
		chunk['RetractionDate'] = pd.to_datetime(chunk['RetractionDate'], errors='coerce')
		chunk['daysinbetween'] = chunk['RetractionDate'] - chunk['OriginalPaperDate']

		processed_chunks.append(chunk)
		out = pd.concat(processed_chunks, ignore_index=True)
		out.index.name = "ID"

	return out

def get_unique_subjects(df):
	subjects = {}

	for i in range(len(df)):
		rowSubjects = df.iloc[i]['Subject'].split(';')

		for s in rowSubjects:
			if s in subjects.keys():
				subjects[s] += 1
			elif s != '':
				subjects[s] = 1		

	out = {
		"count": [],
		"subject": []
	}
	index = []

	id = 0
	for key in subjects.keys():
		index.append(id)
		out["count"].append(subjects[key])
		out["subject"].append(key)
		id += 1
	out = pd.DataFrame(out, index=index)
	out.index.name = "ID"
	return out