# tests/test_data_loader.py
import pandas as pd
import numpy as np
import os
import pytest

def test_data_file_exists():
    """Test that the main data file exists."""
    assert os.path.exists('data/raw/ethiopia_fi_unified_data.csv'), "Data file not found"

def test_data_loading():
    """Test that data loads correctly."""
    df = pd.read_csv('data/raw/ethiopia_fi_unified_data.csv')
    assert len(df) > 0, "Data file is empty"
    assert 'record_type' in df.columns, "record_type column missing"

def test_record_types():
    """Test that record types are valid."""
    df = pd.read_csv('data/raw/ethiopia_fi_unified_data.csv')
    valid_types = ['observation', 'event', 'impact_link', 'target']
    assert set(df['record_type'].unique()).issubset(set(valid_types)), "Invalid record types found"

def test_reference_codes():
    """Test that reference codes file exists."""
    assert os.path.exists('data/raw/reference_codes.csv'), "Reference codes file not found"

def test_forecast_files():
    """Test that forecast files exist."""
    forecast_files = [
        'forecast_base_2025_2027.csv',
        'forecast_optimistic_2025_2027.csv',
        'forecast_pessimistic_2025_2027.csv'
    ]
    for f in forecast_files:
        path = f'data/processed/{f}'
        if os.path.exists(path):
            df = pd.read_csv(path)
            assert len(df) > 0, f"{f} is empty"

def test_dashboard_exists():
    """Test that dashboard file exists."""
    assert os.path.exists('dashboard/app.py'), "Dashboard file not found"

def test_notebooks_exist():
    """Test that all task notebooks exist."""
    notebooks = [
        'task1_data_exploration_and_enrichment',
        'task2_exploratory_data_analysis',
        'task3_event_impact_modeling',
        'task4_forecasting'
    ]
    for nb in notebooks:
        assert os.path.exists(f'notebooks/{nb}.ipynb'), f"{nb}.ipynb not found"