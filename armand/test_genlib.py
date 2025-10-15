from genlib import count, get_unique_values, visualize, multiHotEncoding, delete_empty_columns, iterativeMultiHotEncoding
import pandas as pd
import numpy as np

import unittest
from pandas.testing import assert_frame_equal

class TestGenlib_count(unittest.TestCase):
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
		input_df = pd.DataFrame({'Color': []})

		# 2. Act
		actual_df = count(input_df, 'Color')

		# 3. Assert
		expected_df = pd.DataFrame({
			'Color': [],
			'count': []
		}).astype({'Color': float, 'count': int})
		expected_df.index.name = 'ID'

		assert_frame_equal(actual_df, expected_df)

	def test_raises_error_for_missing_column(self):
		"""Tests that the function correctly raises a KeyError for a column that doesn't exist."""
		# 1. Arrange
		input_df = pd.DataFrame({'A': [1, 2, 3]})

		# 2. Act & Assert: Use a context manager to confirm an error is raised
		with self.assertRaises(KeyError):
			count(input_df, 'NonExistentColumn')

class TestGenlib_get_unique_values(unittest.TestCase):
	def test_standard_case_with_semicolon(self):
		"""Tests the primary functionality with repeated and unique values."""
		# 1. ARRANGE
		data = {'topics': [
			'Science;Math',
			'History',
			'Science;History',
			'Math;Science'
		]}
		input_df = pd.DataFrame(data)

		expected_data = {
			'topics': ['Science', 'Math', 'History'],
			'count': [3, 2, 2]
		}
		expected_df = pd.DataFrame(expected_data)
		expected_df.index.name = "ID"

		# 2. ACT
		actual_df = get_unique_values(input_df, 'topics')

		# 3. ASSERT
		# Sort values to ensure consistent order for comparison
		expected_df = expected_df.sort_values(by=['count', 'topics'], ascending=[False, True]).reset_index(drop=True)
		expected_df.index.name = "ID"
		actual_df = actual_df.sort_values(by=['count', 'topics'], ascending=[False, True]).reset_index(drop=True)
		actual_df.index.name = "ID"
		assert_frame_equal(actual_df, expected_df)

	def test_handles_empty_dataframe(self):
		"""Tests that an empty DataFrame input produces a correct empty output."""
		# 1. ARRANGE
		input_df = pd.DataFrame({'topics': []}, dtype=object)
		

		# 2. ACT
		actual_df = get_unique_values(input_df, 'topics')

		# 3. ASSERT
		expected_df = pd.DataFrame({
			'topics': [],
			'count': []
		}).astype({'topics': 'object', 'count': int})
		expected_df.index.name = "ID"

		assert_frame_equal(actual_df, expected_df)

	def test_ignores_missing_values(self):
		"""Tests that rows with NaN are correctly dropped and ignored."""
		# 1. ARRANGE
		data = {'skills': ['Python;SQL', np.nan, 'SQL;R', 'Python']}
		input_df = pd.DataFrame(data)

		# 2. ACT
		actual_df = get_unique_values(input_df, 'skills')
		actual_df = actual_df.sort_values(by='skills').reset_index(drop=True)

		# 3. ASSERT
		# Sorting is important because value_counts order can be ambiguous for ties
		expected_df = pd.DataFrame({'skills': ['Python', 'SQL', 'R'], 'count': [2, 2, 1]})
		expected_df.index.name = "ID"
		expected_df = expected_df.sort_values(by='skills').reset_index(drop=True)

		assert_frame_equal(actual_df, expected_df)

	def test_with_custom_separator(self):
		"""Tests functionality with a comma as a custom separator."""
		# 1. ARRANGE
		data = {'colors': ['Red,Blue', 'Green', 'Blue,Green']}
		input_df = pd.DataFrame(data)

		expected_data = {'colors': ['Blue', 'Green', 'Red'], 'count': [2, 2, 1]}
		expected_df = pd.DataFrame(expected_data)
		expected_df.index.name = "ID"

		# 2. ACT
		actual_df = get_unique_values(input_df, 'colors', split_str=',')

		# 3. ASSERT
		expected_df = expected_df.sort_values(by='colors').reset_index(drop=True)
		expected_df.index.name = "ID"
		actual_df = actual_df.sort_values(by='colors').reset_index(drop=True)
		actual_df.index.name = "ID"
		assert_frame_equal(actual_df, expected_df)

	def test_handles_whitespace_and_empty_splits(self):
		"""
		Tests that whitespace is preserved and empty strings are counted,
		as per the current function's logic.
		"""
		# 1. ARRANGE
		input_df = pd.DataFrame({'langs': [' Python ;Java', 'Go;', 'C#;;Go']})

		# 2. ACT
		actual_df = get_unique_values(input_df, 'langs')
		actual_df = actual_df.sort_values(by=['count', 'langs'], ascending=[False, True]).reset_index(drop=True)

		# 3. ASSERT
		expected_df = pd.DataFrame({
			'langs': ['Go', 'Python', 'Java', 'C#'],
			'count': [2, 1, 1, 1]
		})
		expected_df.index.name = "ID"
		expected_df = expected_df.sort_values(by=['count', 'langs'], ascending=[False, True]).reset_index(drop=True)

		assert_frame_equal(actual_df, expected_df)

	def test_raises_error_for_non_string_column(self):
		"""Tests that an AttributeError is raised for numeric columns."""
		# 1. ARRANGE
		input_df = pd.DataFrame({'numbers': [100, 200, 300]})

		# 2. ACT & 3. ASSERT
		with self.assertRaises(AttributeError):
			get_unique_values(input_df, 'numbers')



# This allows running the tests directly
if __name__ == '__main__':
	unittest.main()