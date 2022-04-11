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
rounds = st.selectbox('Select number of rounds', [x for x in range(1, 11)])

if num_players and match_type and rounds:
    players = [f'Player {x}' for x in range(1, num_players + 1)]
    game_size = 4 if match_type == 'Doubles' else 2
    matches = num_players // game_size + \
        1 if num_players % game_size != 0 else num_players // game_size
    history = {}
    for player in players:
        history[player] = {'teammates': [], 'opponents': []}
    # history = {'Player 1': {'teammates': ['Player 3', 'Player 4', 'Player 5'], 'opponents': ['Player 3','Player 6', 'Player 7']}}

    f'Calculating {matches * rounds} matches...'

    # Initialize progress bar
    bar = st.progress(0)

    for i in range(rounds):
        # Iterate over desired rounds

        # Get results and updated history each time
        results, history = arrange_players(
            players, game_size, history, iterations=10)

        # Update the progress bar with each iteration.
        bar.progress((i + 1) / rounds)

        # Output results
        st.subheader(f'Round {i + 1}')
        st.dataframe(results)  # add a styler?

# Pseudocode
# Determine random weights for playing with same player (2) or against same player (1)
# Do X iterations, and find a combo with minimum weights
# Store history of who played with who and who played against who
# Use this history to calculate score
