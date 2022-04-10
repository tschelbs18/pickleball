"""
# Pickleball App
# Dev log: need to input rounds as an input - generate multiple distinct random rounds to maximize player coverage
"""

import streamlit as st
import pandas as pd
import time
import random
from helper import arrange_players

st.title("🎾 Lori's Pickleball App 🎾")

st.subheader('Fill out the form below to generate matchups')
num_players = st.selectbox('Input the number of players from 4 to 40', [
    x for x in range(4, 41)])
f'You selected: {num_players} players'
match_type = st.selectbox('Select the match type', ['', 'Singles', 'Doubles'])

if num_players and match_type:
    players = [f'Player {x}' for x in range(1, num_players + 1)]
    game_size = 4 if match_type == 'Doubles' else 2
    matches = num_players // game_size + \
        1 if num_players % game_size != 0 else num_players // game_size

    f'Calculating {matches} matches...'

    random.shuffle(players)
    results = arrange_players(players, game_size)

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(10):
        # Update the progress bar with each iteration.
        # latest_iteration.text(f'Iteration {i+1}')
        bar.progress((i + 1) * 10)
        time.sleep(0.1)

    st.subheader('Random Matches')
    st.dataframe(results)  # add a styler?

# Pseudocode
# Add rounds as an input
# Determine iterations based on rounds
# Determine random weights for playing with same player or against same player
# Do X iterations, and find a combo with minimum weights
# Store history of who played with who and who played against who
# Use this history to calculate score
