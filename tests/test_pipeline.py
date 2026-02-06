"""
Unit tests for data cleaning module
"""
import unittest
import pandas as pd
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline.data_cleaning import DataCleaner


class TestDataCleaner(unittest.TestCase):
    """Test cases for DataCleaner class"""
    
    def setUp(self):
        """Set up test data"""
        self.cleaner = DataCleaner()
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 2, 3, 4],
            'name': ['Alice', 'Bob', 'Bob', 'Charlie', None],
            'value': [10.5, 20.0, 20.0, None, 40.0]
        })
    
    def test_remove_duplicates(self):
        """Test duplicate removal"""
        result = self.cleaner.remove_duplicates(self.sample_data)
        self.assertEqual(len(result), 4)
    
    def test_handle_missing_values_drop(self):
        """Test missing value handling with drop strategy"""
        result = self.cleaner.handle_missing_values(self.sample_data, strategy='drop')
        self.assertEqual(len(result), 3)
    
    def test_handle_missing_values_fill(self):
        """Test missing value handling with fill strategy"""
        result = self.cleaner.handle_missing_values(self.sample_data, strategy='fill')
        self.assertEqual(result['value'].isnull().sum(), 0)
    
    def test_standardize_text(self):
        """Test text standardization"""
        result = self.cleaner.standardize_text(self.sample_data, ['name'])
        # Check non-null values are lowercase
        non_null_names = result['name'].dropna()
        self.assertTrue((non_null_names.str.islower()).all())


class TestDataValidator(unittest.TestCase):
    """Test cases for DataValidator class"""
    
    def setUp(self):
        """Set up test data"""
        from pipeline.data_validation import DataValidator
        self.validator = DataValidator(required_columns=['id', 'name'])
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'value': [10, 20, 30]
        })
    
    def test_validate_schema(self):
        """Test schema validation"""
        result = self.validator.validate_schema(self.sample_data)
        self.assertTrue(result['has_required_columns'])
        self.assertEqual(len(result['missing_columns']), 0)
    
    def test_check_data_quality(self):
        """Test data quality check"""
        result = self.validator.check_data_quality(self.sample_data)
        self.assertEqual(result['total_rows'], 3)
        self.assertEqual(result['total_columns'], 3)
        self.assertEqual(result['missing_cells'], 0)


if __name__ == '__main__':
    unittest.main()
