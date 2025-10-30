import unittest
import pandas as pd
import numpy as np

# Import the functions you want to test
from libs.cleaning.hotEncoding import singleHotEncoding, multiHotEncoding, iterativeMultiHotEncoding, allHotencoding

class TestHotEncoding(unittest.TestCase):

    def setUp(self):
        """
        This method is called before each test. It sets up a sample DataFrame
        with various edge cases to test against.
        """
        self.sample_data = {
            'id': [1, 2, 3, 4],
            'color': ['Red', 'Blue', np.nan, 'Blue'],  # For single-hot encoding
            'genres': [
                'Action;Adventure',        # Standard case
                'Adventure; Fantasy',      # Inconsistent whitespace
                'Comedy;;Action',          # Double separator
                np.nan                     # Missing value
            ],
            'tags': ['Fast-Paced', 'Slow', 'Fast-Paced;Funny', ''] # Another multi-hot column
        }
        self.df = pd.DataFrame(self.sample_data)

    def test_singleHotEncoding(self):
        """Tests the single-hot encoding function."""
        encoded_df = singleHotEncoding(self.df.copy(), ['color'])
        
        # Check if the correct columns were created
        expected_columns = ['color_Blue', 'color_Red', 'color_nan']
        for col in expected_columns:
            self.assertIn(col, encoded_df.columns)
            
        # Check the values for the row with NaN
        self.assertEqual(encoded_df.loc[2, 'color_nan'], 1)
        self.assertEqual(encoded_df.loc[2, 'color_Blue'], 0)
        
        # Check a normal row
        self.assertEqual(encoded_df.loc[0, 'color_Red'], 1)
        self.assertEqual(encoded_df.loc[0, 'color_nan'], 0)

    def test_multiHotEncoding(self):
        """
        Tests the multi-hot encoding function for a single column.
        Verifies handling of NaN, whitespace, double separators, and case.
        """
        encoded_df = multiHotEncoding(self.df.copy(), 'genres', ';')
        
        # Check if the correct columns were created (should be lowercase)
        expected_columns = ['genres_action', 'genres_adventure', 'genres_comedy', 'genres_fantasy']
        for col in expected_columns:
            self.assertIn(col, encoded_df.columns)

        # Verify row with inconsistent whitespace and double separator
        self.assertEqual(encoded_df.loc[1, 'genres_adventure'], 1)
        self.assertEqual(encoded_df.loc[1, 'genres_fantasy'], 1)
        self.assertEqual(encoded_df.loc[2, 'genres_comedy'], 1)
        self.assertEqual(encoded_df.loc[2, 'genres_action'], 1)
        
        # Verify row with NaN is all zeros
        self.assertEqual(encoded_df.loc[3, 'genres_action'], 0)
        self.assertEqual(encoded_df.loc[3, 'genres_fantasy'], 0)

    def test_iterativeMultiHotEncoding(self):
        """Tests the wrapper for multi-hot encoding multiple columns."""
        encoded_df = iterativeMultiHotEncoding(self.df.copy(), ['genres', 'tags'], ';')
        
        # Check for columns from both original fields
        self.assertIn('genres_action', encoded_df.columns)
        self.assertIn('tags_funny', encoded_df.columns)
        self.assertNotIn('genres', encoded_df.columns) # Original should be dropped
        self.assertNotIn('tags', encoded_df.columns)

    def test_allHotencoding(self):
        """Tests the main function combining both encoding types."""
        encoded_df = allHotencoding(self.df.copy(), ['color'], ['genres', 'tags'], ';')
        
        # Check for a representative column from each transformation
        self.assertIn('color_Red', encoded_df.columns)
        self.assertIn('color_nan', encoded_df.columns)
        self.assertIn('genres_adventure', encoded_df.columns)
        self.assertIn('tags_fast-paced', encoded_df.columns)
        
        # Check that original columns were dropped
        self.assertNotIn('color', encoded_df.columns)
        self.assertNotIn('genres', encoded_df.columns)
        self.assertNotIn('tags', encoded_df.columns)
        
        # Verify a specific row's data
        self.assertEqual(encoded_df.loc[0, 'color_Red'], 1)
        self.assertEqual(encoded_df.loc[0, 'genres_action'], 1)
        self.assertEqual(encoded_df.loc[0, 'tags_fast-paced'], 1)
        self.assertEqual(encoded_df.loc[0, 'tags_funny'], 0)

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)