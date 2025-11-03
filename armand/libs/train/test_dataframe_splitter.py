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
        x, y = split_dataframe(self.df, self.target_df['target'])
        
        self.assertEqual(len(x.train), 60)
        self.assertEqual(len(y.train), 60)
        
        self.assertEqual(len(x.val), 20)
        self.assertEqual(len(y.val), 20)
        
        self.assertEqual(len(x.test), 20)
        self.assertEqual(len(y.test), 20)

    def test_determinism(self):
        """Test if the same random_state produces the same split."""
        x1, y1 = split_dataframe(self.df, self.target_df['target'], random_state=42)
        x2, y2 = split_dataframe(self.df, self.target_df['target'], random_state=42)
        
        # Use pandas testing utility to check for exact equality
        pd.testing.assert_frame_equal(x1.train, x2.train)
        pd.testing.assert_frame_equal(x1.test, x2.test)

    def test_stratification(self):
        """Test if the class distribution is maintained across splits."""
        x, y = split_dataframe(self.df, self.target_df['target'])
        
        original_dist = self.target_df['target'].value_counts(normalize=True)
        train_dist = y.train.value_counts(normalize=True)
        val_dist = y.val.value_counts(normalize=True)
        
        # Check that the distribution in train and validation sets is close to the original
        pd.testing.assert_series_equal(original_dist, train_dist, check_names=False)
        pd.testing.assert_series_equal(original_dist, val_dist, check_names=False)

    def test_no_overlap(self):
        """Test that there is no overlap between the train, validation, and test sets."""
        x, y = split_dataframe(self.df, self.target_df['target'])
        
        train_indices = set(x.train.index)
        val_indices = set(x.val.index)
        test_indices = set(x.test.index)
        
        # Check that the intersection of any two sets is empty
        self.assertTrue(train_indices.isdisjoint(val_indices))
        self.assertTrue(train_indices.isdisjoint(test_indices))
        self.assertTrue(val_indices.isdisjoint(test_indices))

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)