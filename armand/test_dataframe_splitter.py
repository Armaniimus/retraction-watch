import unittest
import pandas as pd
import numpy as np

# Import the function to be tested
from dataframe_splitter import split_dataframe

class TestDataFrameSplitter(unittest.TestCase):

    def setUp(self):
        """
        Create a sample DataFrame that runs before each test.
        It has 100 rows to make percentage splits easy to verify.
        """
        data = {
            'feature1': range(100),
            'feature2': np.random.rand(100)
        }
        target_data = {'target': ['A'] * 50 + ['B'] * 50} # Balanced classes for stratification test
        
        self.df = pd.DataFrame(data)
        self.target_df = pd.DataFrame(target_data)

    def test_split_shapes(self):
        """Test if the output DataFrames have the correct shapes (60/20/20 split)."""
        result = split_dataframe(self.df, self.target_df['target'])
        
        self.assertEqual(len(result['x']['train']), 60)
        self.assertEqual(len(result['y']['train']), 60)
        
        self.assertEqual(len(result['x']['validate']), 20)
        self.assertEqual(len(result['y']['validate']), 20)
        
        self.assertEqual(len(result['x']['test']), 20)
        self.assertEqual(len(result['y']['test']), 20)

    def test_determinism(self):
        """Test if the same random_state produces the same split."""
        result1 = split_dataframe(self.df, self.target_df['target'], random_state=42)
        result2 = split_dataframe(self.df, self.target_df['target'], random_state=42)
        
        # Use pandas testing utility to check for exact equality
        pd.testing.assert_frame_equal(result1['x']['train'], result2['x']['train'])
        pd.testing.assert_frame_equal(result1['x']['test'], result2['x']['test'])

    def test_stratification(self):
        """Test if the class distribution is maintained across splits."""
        result = split_dataframe(self.df, self.target_df['target'])
        
        original_dist = self.target_df['target'].value_counts(normalize=True)
        train_dist = result['y']['train'].value_counts(normalize=True)
        val_dist = result['y']['validate'].value_counts(normalize=True)
        
        # Check that the distribution in train and validation sets is close to the original
        pd.testing.assert_series_equal(original_dist, train_dist, check_names=False)
        pd.testing.assert_series_equal(original_dist, val_dist, check_names=False)

    def test_no_overlap(self):
        """Test that there is no overlap between the train, validation, and test sets."""
        result = split_dataframe(self.df, self.target_df['target'])
        
        train_indices = set(result['x']['train'].index)
        val_indices = set(result['x']['validate'].index)
        test_indices = set(result['x']['test'].index)
        
        # Check that the intersection of any two sets is empty
        self.assertTrue(train_indices.isdisjoint(val_indices))
        self.assertTrue(train_indices.isdisjoint(test_indices))
        self.assertTrue(val_indices.isdisjoint(test_indices))

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)