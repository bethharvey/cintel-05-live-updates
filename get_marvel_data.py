"""
----------------------------
Marvel API Information
----------------------------

Go to: https://developer.marvel.com/

Sign up for a free account to get your public and private API keys.

The Marvel API allows up to 3000 calls per day.

"""

# Standard Library
from pathlib import Path
import os

# External Packages
import pandas as pd
from collections import deque
from dotenv import load_dotenv
from marvel import Marvel

# Local Imports
from util_logger import setup_logger

# Set up a file logger
logger, log_filename = setup_logger(__file__)

def get_public_API_key():
    # Keep secrets in a .env file - load it, read the values.
    # Load environment variables from .env file
    load_dotenv()
    m_public_key = os.getenv("MARVEL_PUBLIC_KEY")
    return m_public_key

def get_private_API_key():
    load_dotenv()
    m_private_key = os.getenv('MARVEL_PRIVATE_KEY')
    return m_private_key

# Initialize Marvel API object
m = Marvel(get_public_API_key(), get_private_API_key())


# Get list of characters from name
def get_character_names(character_name):
    all_character_info = m.characters.all(nameStartsWith = character_name)
    character_names = []
    for i in range(len(all_character_info['data']['results'])):
        name = all_character_info['data']['results'][i]['name']
        character_names.append(name)
    return character_names


# Get character descriptions
def get_character_descriptions(character_name):
    all_character_info = m.characters.all(nameStartsWith = character_name)
    character_descriptions = []
    for i in range(len(all_character_info['data']['results'])):
        description = all_character_info['data']['results'][i]['description']
        character_descriptions.append(description)
    return character_descriptions


# Get number of comics a character has appeared in
def get_number_of_appearances(character_name):
    all_character_info = m.characters.all(nameStartsWith = character_name)
    character_appearances = []
    for i in range(len(all_character_info['data']['results'])):
        num_appearances = (all_character_info['data']['results'][i]['comics']['available'] + 
                        all_character_info['data']['results'][i]['series']['available'] + 
                        all_character_info['data']['results'][i]['events']['available'] + 
                        all_character_info['data']['results'][i]['stories']['available'])
        character_appearances.append(num_appearances)
    return character_appearances


# Get character ID using character name
def get_character_id(character_name):
    all_characters = m.characters.all(name = character_name)
    character_ids = []
    for i in range(len(all_characters['data']['results'])):
        character_id = all_characters['data']['results'][i]['id']
        character_ids.append(character_id)
    return character_ids


# Create CSV with column headings
def init_character_file(file_path):
    df_empty = pd.DataFrame(columns=['Character Name', 'Variant Name', 'Number of Appearances Available', 'Character Description (If Available)'])
    df_empty.to_csv(file_path, index=False)


# Get character info for specific characters and add to CSV
def get_character_info():
    character_list = ['Spider-Man', 
                      'Captain America', 
                      'Black Widow', 
                      'Iron Man', 
                      'Thor', 
                      'Captain Marvel']
    
    records_deque = deque()

    fp = Path(__file__).parent.joinpath("marvel_character_data.csv")

        # Check if the file exists, if not, create it with only the column headings
    if not os.path.exists(fp):
            init_character_file(fp)

    for character in character_list:
        character_name = character
        specific_name_list = get_character_names(character)
        number_appearances_list = get_number_of_appearances(character)
        character_description_list = get_character_descriptions(character)
        for i in range(len(specific_name_list)):
            new_record = {
                'Character Name': character_name,
                'Variant Name': specific_name_list[i],
                'Number of Appearances Available': number_appearances_list[i],
                'Character Description (If Available)': character_description_list[i],
                }
            records_deque.append(new_record)
        # Use the deque to make a DataFrame
        df = pd.DataFrame(records_deque)
        df.to_csv(fp, index=False, mode="w")

# get_character_info()




# def get_comics_list(character_id_list):
#     date_list = []
#     for character_id in character_id_list:
#         character_info = m.characters.comics(character_id)
#         for i in range(len(character_info['data']['results'])):
#             comic_date = character_info['data']['results'][i]['dates'][1]['date']
#             date_list.append(comic_date)
#         return date_list



