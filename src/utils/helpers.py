"""
Pipeline Utility Functions
"""
import pandas as pd
import os
from typing import List


def list_csv_files(directory: str) -> List[str]:
    """
    List all CSV files in a directory
    
    Args:
        directory: Path to directory
        
    Returns:
        List of CSV filenames
    """
    if not os.path.exists(directory):
        return []
        
    return [f for f in os.listdir(directory) if f.endswith('.csv')]


def create_directory_if_not_exists(directory: str) -> None:
    """
    Create directory if it doesn't exist
    
    Args:
        directory: Path to directory
    """
    os.makedirs(directory, exist_ok=True)


def get_csv_sample(filepath: str, n_rows: int = 5) -> pd.DataFrame:
    """
    Get a sample of rows from a CSV file
    
    Args:
        filepath: Path to CSV file
        n_rows: Number of rows to sample
        
    Returns:
        DataFrame with sampled rows
    """
    return pd.read_csv(filepath, nrows=n_rows)


def merge_csv_files(filepaths: List[str], output_path: str) -> pd.DataFrame:
    """
    Merge multiple CSV files into one
    
    Args:
        filepaths: List of CSV file paths
        output_path: Path for merged output file
        
    Returns:
        Merged DataFrame
    """
    dfs = [pd.read_csv(fp) for fp in filepaths]
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.to_csv(output_path, index=False)
    return merged_df
