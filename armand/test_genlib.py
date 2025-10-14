import unittest
from genlib import get_csv, save_csv, count, count_total_values, get_unique_values, add_counted_dates, print_dataframe, visualize, multiHotEncoding, delete_empty_columns, iterativeMultiHotEncoding
import pandas as pd
from pandas.testing import assert_frame_equal

class TestGenlib(unittest.TestCase):
	"""A class to test the 'count' function."""

	def test_basic_counting(self):
		"""Tests the function with a simple, standard case."""
		# 1. Arrange: Set up the input data
		input_data = {'Fruit': ['Apple', 'Orange', 'Apple', 'Banana', 'Orange', 'Apple']}
		input_df = pd.DataFrame(input_data)

		# 2. Act: Call the function we are testing
		actual_df = count(input_df, 'Fruit')

		# 3. Assert: Define the expected outcome and check if it matches the actual outcome
		expected_index = pd.Index([0, 1, 2], name='ID')
		expected_columns = {"Fruit": ['Apple', 'Orange', 'Banana'], 'count': [3, 2, 1]}
		expected_df = pd.DataFrame(expected_columns, index=expected_index)

		# Use pandas' specific testing tool for an accurate comparison
		assert_frame_equal(actual_df, expected_df)

	def test_with_empty_dataframe(self):
		# 1. Arrange		
		input_df = pd.DataFrame({'Color': []}, dtype='object')

		# 2. Act
		actual_df = count(input_df, 'Color')

		# 3. Assert
		expected_df = pd.DataFrame({
			'Color': [],
			'count': []
		}).astype({'Color': 'object', 'count': int})
		expected_df.index.name = 'ID'

		assert_frame_equal(actual_df, expected_df)

	def test_raises_error_for_missing_column(self):
		"""Tests that the function correctly raises a KeyError for a column that doesn't exist."""
		# 1. Arrange
		input_df = pd.DataFrame({'A': [1, 2, 3]})

		# 2. Act & Assert: Use a context manager to confirm an error is raised
		with self.assertRaises(KeyError):
			count(input_df, 'NonExistentColumn')


# This allows running the tests directly
if __name__ == '__main__':
	unittest.main()