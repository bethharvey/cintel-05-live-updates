"""
Purpose: Display output for Marvel dataset.

@imports shiny.ui as ui
@imports shinywidgets.output_widget for interactive charts
"""
from shiny import ui
from shinywidgets import output_widget


def get_marvel_outputs():
    return ui.panel_main(
        ui.h2("Main Panel with Reactive Output"),
        ui.tags.hr(),
        ui.tags.section(
            ui.h3('Did you know?'),
            ui.tags.br(),
            ui.output_text('marvel_character_string'),
            ui.tags.br(),
            output_widget('marvel_character_chart'),
            ui.tags.br(),
            ui.h3('Filtered Character Summary Table'),
            ui.output_table('marvel_character_table'),
            ui.tags.br(),
        ),
    )