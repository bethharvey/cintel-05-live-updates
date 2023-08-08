""" 
Purpose: Provide continuous and reactive output for the MT Cars dataset.

- Use inputs from the UI Sidebar to filter the dataset.
- Update reactive outputs in the UI Main Panel.

"""

# Standard Library
from pathlib import Path

# External Libraries
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import aes, geom_point, ggplot, ggtitle
import plotly.express as px
from shiny import render, reactive
from shinywidgets import render_widget
from shiny.types import ImgData

# Local Imports
from marvel_get_basics import get_marvel_df
from util_logger import setup_logger

# Set up a global logger for this file
logger, logname = setup_logger(__name__)

def get_marvel_server_functions(input, output, session):

    reactive_character = reactive.Value('Spider-Man')
    reactive_df = reactive.Value()

    csv_marvel = (
        Path(__file__).parent.joinpath('marvel_character_data.csv')
    )
    original_df = pd.read_csv(csv_marvel)
    total_count = len(original_df)


    @reactive.Effect
    @reactive.event(input.MARVEL_CHARACTER_SELECT)
    def _():
        """Update the filtered dataframe when the user changes the character choice."""

        # With Shiny, we call the copy() function to make a copy of the original dataframe
        # This is to signal that a value has truly changed
        df = original_df.copy()

        input_character = input.MARVEL_CHARACTER_SELECT()

        """
        Filter the dataframe to just those greater than or equal to the min
        and less than or equal to the max
        Note: The ampersand (&) is the Python operator for AND
        The column name is in quotes and is "mpg".
        You must be familiar with the dataset to know the column names.
        """

        filtered_df = df[(df['Character Name'] == input_character)]

        # Set the reactive values
        # These are things that will change when the user changes the inputs
        # We use them to drive the reactive outputs
        # First, there's the filtered dataframe
        reactive_df.set(filtered_df)

    @reactive.Effect
    @reactive.event(input.MARVEL_CHARACTER_SELECT)
    def _():
        """Set two reactive values (the location and temps df) when user changes location"""
        reactive_character.set(input.MARVEL_CHARACTER_SELECT())
        df = get_marvel_df()
        logger.info(f"init reactive_character_df len: {len(df)}")

    @output
    @render.text
    def marvel_character_string():
        """Return a string based on selected character."""
        logger.info("marvel_character_string starting")
        selected = reactive_character.get()
        df = get_marvel_df()
        df_character = df[df['Character Name'] == reactive_character.get()]
        character_length = len(df_character)
        num_appearances = sum(df_character['Number of Appearances Available'])
        line1 = f'There are {character_length} different characters whose name starts with {selected}!'
        line2 = f'{selected} characters have appeared {num_appearances} times in the comics in this database.'
        # line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}"
        logger.info(f"{message}")
        return message

    @output
    @render.table
    def marvel_character_table():
        df = get_marvel_df()
        # Filter the data based on the selected character
        df_character = df[df['Character Name'] == reactive_character.get()]
        logger.info(f"Rendering character table with {len(df_character)} rows")
        return df_character
    

    return [
        marvel_character_string,
        marvel_character_table
        ]
    