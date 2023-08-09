"""
----------------------------
Marvel API Information
----------------------------

Go to: https://developer.marvel.com/

Sign up for a free account to get your public and private API keys.

The Marvel API allows up to 3000 calls per day.

"""

# Standard Library
import asyncio
from pathlib import Path
import os

# External Packages
import pandas as pd
from collections import deque
from dotenv import load_dotenv

# Local Imports
from util_logger import setup_logger
from fetch import fetch_from_url

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


# Get list of characters from name
async def get_character_names(character_name):
    public_key = get_public_API_key()
    marvel_api_url = f'https://gateway.marvel.com:443/v1/public/characters?nameStartsWith={character_name}&apikey={public_key}'
    result = await fetch_from_url(marvel_api_url, 'json')
    all_character_info = result.data['results']
    character_names = []
    for i in range(len(all_character_info)):
        name = all_character_info[i]['name']
        character_names.append(name)
    return character_names


# Get character descriptions
async def get_character_descriptions(character_name):
    public_key = get_public_API_key()
    marvel_api_url = f'https://gateway.marvel.com:443/v1/public/characters?nameStartsWith={character_name}&apikey={public_key}'
    result = await fetch_from_url(marvel_api_url)
    all_character_info = result.data['results']
    character_descriptions = []
    for i in range(len(all_character_info)):
        description = all_character_info[i]['description']
        character_descriptions.append(description)
    return character_descriptions


# Get number of comics a character has appeared in
async def get_number_of_appearances(character_name):
    public_key = get_public_API_key()
    marvel_api_url = f'https://gateway.marvel.com:443/v1/public/characters?nameStartsWith={character_name}&apikey={public_key}'
    result = await fetch_from_url(marvel_api_url)
    all_character_info = result.data['results']
    character_appearances = []
    for i in range(len(all_character_info)):
        num_appearances = (all_character_info[i]['comics']['available'] + 
                        all_character_info[i]['series']['available'] + 
                        all_character_info['events']['available'] + 
                        all_character_info['stories']['available'])
        character_appearances.append(num_appearances)
    return character_appearances


# Create CSV with column headings
def init_character_file(file_path):
    df_empty = pd.DataFrame(columns=['Character Name', 'Variant Name', 'Number of Appearances Available', 'Character Description (If Available)'])
    df_empty.to_csv(file_path, index=False)


# Get character info for specific characters and add to CSV
async def get_character_info():
    try:
        character_list = ['Spider-Man', 
                      'Captain America', 
                      'Black Widow', 
                      'Iron Man', 
                      'Thor', 
                      'Captain Marvel']
        update_interval = 10000  # Update every 10000 seconds
        total_runtime = 1  # Total runtime maximum of 15 minutes
        num_updates = 1  # Keep the most recent 1 readings
        logger.info(f"update_interval: {update_interval}")
        logger.info(f"total_runtime: {total_runtime}")
        logger.info(f"num_updates: {num_updates}")
    
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

            # Wait for update_interval seconds before the next reading
            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_location: {e}")

# get_character_info()
