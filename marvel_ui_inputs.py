"""
Purpose: Provide user interaction options for Marvel dataset.

"""

from shiny import ui

# Define the UI inputs and include selection options

def get_marvel_inputs():
    return ui.panel_sidebar(
        ui.h2('Marvel Data Interaction'),
        ui.tags.hr(),
        ui.input_select(
            id = 'MARVEL_CHARACTER_SELECT',
            label = 'Select a character',
            choices = ['Spider-Man', 'Captain America', 'Black Widow', 'Iron Man', 'Thor', 'Captain Marvel'],
            selected = 'Spider-Man',
        )
    )