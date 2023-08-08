"""
Purpose: 

Provide basic non-reactive functions to support 
the Marvel interactive analytics dashboard.

"""

# Python Standard Library 
import pathlib
import os

# External Packages
import pandas as pd  # pip install pandas

# Local Imports
from util_logger import setup_logger

# Set up a logger for this file (see the logs folder to help with debugging).
logger, logname = setup_logger(__name__)

def get_marvel_df():
    """Return Marvel pandas Dataframe."""
    p = pathlib.Path(__file__).parent.joinpath("marvel_character_data.csv")
    # logger.info(f"Reading data from {p}")
    df = pd.read_csv(p)
    return df