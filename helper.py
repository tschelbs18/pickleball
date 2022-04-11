from re import L
import pandas as pd
from random import shuffle


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def combine_doubles(teams):
    '''Combine a 4 column df to a 2 column df for easier display of teams'''
    if len(teams) == 0:
        # If there's no players, return an empty DF
        df = pd.DataFrame()
        df['Team 1'] = []
        df['Team 2'] = []
    else:
        # If there are players, return a combined 2 team df
        df = pd.DataFrame(
            teams, columns=['Team 1 (1)', 'Team 1 (2)', 'Team 2 (1)', 'Team 2 (2)'])
        df['Team 1'] = df[['Team 1 (1)', 'Team 1 (2)']].agg(
            ', '.join, axis=1)
        df['Team 2'] = df[['Team 2 (1)', 'Team 2 (2)']].agg(
            ', '.join, axis=1)
        df.drop(df.columns[[0, 1, 2, 3]], axis=1, inplace=True)
    return df


def check_teammate(history, player1, player2):
    return player2 in history[player1].get('teammates')


def check_opponent(history, player1, player2):
    return player2 in history[player1].get('opponents')


def score_overlap(df, history):
    '''Calculate overlap score for a df given the history'''
    score = 0
    teammate_weight = 2
    opponent_weight = 1
    if len(history) == 0:
        return score
    for index, row in df.iterrows():
        players = row['Team 1'].split(', ') + row['Team 2'].split(', ')
        if len(players) == 2:
            if check_opponent(history, players[0], players[1]):
                score += opponent_weight
        elif len(players) == 3:
            if check_teammate(history, players[0], players[1]):
                score += teammate_weight
            if check_opponent(history, players[0], players[2]):
                score += opponent_weight
            if check_opponent(history, players[1], players[2]):
                score += opponent_weight
        elif len(players) == 4:
            if check_teammate(history, players[0], players[1]):
                score += teammate_weight
            if check_teammate(history, players[2], players[3]):
                score += teammate_weight
            if check_opponent(history, players[0], players[2]):
                score += opponent_weight
            if check_opponent(history, players[0], players[3]):
                score += opponent_weight
            if check_opponent(history, players[1], players[2]):
                score += opponent_weight
            if check_opponent(history, players[1], players[3]):
                score += opponent_weight
    return score


def add_teammate(history, player1, player2):
    history[player1]['teammates'].append(player2)
    history[player2]['teammates'].append(player1)
    return history


def add_opponent(history, player1, player2):
    history[player1]['opponents'].append(player2)
    history[player2]['opponents'].append(player1)
    return history


def history_append(df, history):
    '''Add the finalized round to our existing history'''
    for index, row in df.iterrows():
        players = row['Team 1'].split(', ') + row['Team 2'].split(', ')
        if len(players) == 2:
            history = add_opponent(history, players[0], players[1])
        elif len(players) == 3:
            history = add_teammate(history, players[0], players[1])
            history = add_opponent(history, players[0], players[2])
            history = add_opponent(history, players[1], players[2])
        elif len(players) == 4:
            history = add_teammate(history, players[0], players[1])
            history = add_teammate(history, players[2], players[3])
            history = add_opponent(history, players[0], players[2])
            history = add_opponent(history, players[1], players[2])
            history = add_opponent(history, players[0], players[3])
            history = add_opponent(history, players[1], players[3])
    return history


def build_match(players, game_size):
    '''Build a random match to evaluate overlap score'''
    if len(players) % game_size == 0:
        # Perfectly even player distribution for singles or doubles
        teams = list(chunks(players, game_size))
        if game_size == 2:
            df = pd.DataFrame(teams, columns=['Team 1', 'Team 2'])
        else:
            df = combine_doubles(teams)
    elif len(players) % game_size == 1:
        # One additional player
        if game_size == 2:
            # Create all singles matches and one canadian doubles match
            three = players[0:3]
            players = players[3:]
            teams = list(chunks(players, game_size))
            df = pd.DataFrame(teams, columns=['Team 1', 'Team 2'])
            df2 = pd.DataFrame(
                [[three[0] + ', ' + three[1], three[2]]], columns=['Team 1', 'Team 2'])
            df = pd.concat([df, df2], ignore_index=True)
        elif game_size == 4:
            # Create all doubles matches, 1 singles match, and one canadian doubles match
            five = players[0:5]
            players = players[5:]
            teams = list(chunks(players, game_size))
            df = combine_doubles(teams)
            df2 = pd.DataFrame(
                [[five[0] + ', ' + five[1], five[2]], [five[3], five[4]]], columns=['Team 1', 'Team 2'])
            df = pd.concat([df, df2], ignore_index=True)
    elif len(players) % game_size == 2:
        # Create all doubles matches, 1 singles match
        two = players[0:2]
        players = players[2:]
        teams = list(chunks(players, game_size))
        df = combine_doubles(teams)
        df2 = pd.DataFrame([[two[0], two[1]]], columns=['Team 1', 'Team 2'])
        df = pd.concat([df, df2], ignore_index=True)
    elif len(players) % game_size == 3:
        # Create all doubles matches, 1 canadian doubles match
        three = players[0: 3]
        players = players[3:]
        teams = list(chunks(players, game_size))
        df = combine_doubles(teams)
        df2 = pd.DataFrame(
            [[three[0] + ', ' + three[1], three[2]]], columns=['Team 1', 'Team 2'])
        df = pd.concat([df, df2], ignore_index=True)
    return df.copy()


def arrange_players(players, game_size, history, iterations):
    '''Test different builds to compute min overlap'''
    for i in range(iterations):
        shuffle(players)
        curr_df = build_match(players, game_size)
        curr_score = score_overlap(curr_df, history)
        if curr_score == 0:
            best_df = curr_df
            break
        elif i == 0 or curr_score < min_score:
            best_df = curr_df
            min_score = curr_score

    history = history_append(best_df, history)
    return best_df, history


def og_arrange_players(players, game_size, history):
    '''Arrange players into teams given game size'''
    if len(players) % game_size == 0:
        # Perfectly even player distribution for singles or doubles
        teams = list(chunks(players, game_size))
        if game_size == 2:
            df = pd.DataFrame(teams, columns=['Team 1', 'Team 2'])
        else:
            df = combine_doubles(teams)
    elif len(players) % game_size == 1:
        # One additional player
        if game_size == 2:
            # Create all singles matches and one canadian doubles match
            three = players[0:3]
            players = players[3:]
            teams = list(chunks(players, game_size))
            df = pd.DataFrame(teams, columns=['Team 1', 'Team 2'])
            df2 = pd.DataFrame(
                [[three[0] + ', ' + three[1], three[2]]], columns=['Team 1', 'Team 2'])
            df = pd.concat([df, df2], ignore_index=True)
        elif game_size == 4:
            # Create all doubles matches, 1 singles match, and one canadian doubles match
            five = players[0:5]
            players = players[5:]
            teams = list(chunks(players, game_size))
            df = combine_doubles(teams)
            df2 = pd.DataFrame(
                [[five[0] + ', ' + five[1], five[2]], [five[3], five[4]]], columns=['Team 1', 'Team 2'])
            df = pd.concat([df, df2], ignore_index=True)
    elif len(players) % game_size == 2:
        # Create all doubles matches, 1 singles match
        two = players[0:2]
        players = players[2:]
        teams = list(chunks(players, game_size))
        df = combine_doubles(teams)
        df2 = pd.DataFrame([[two[0], two[1]]], columns=['Team 1', 'Team 2'])
        df = pd.concat([df, df2], ignore_index=True)
    elif len(players) % game_size == 3:
        # Create all doubles matches, 1 canadian doubles match
        three = players[0: 3]
        players = players[3:]
        teams = list(chunks(players, game_size))
        df = combine_doubles(teams)
        df2 = pd.DataFrame(
            [[three[0] + ', ' + three[1], three[2]]], columns=['Team 1', 'Team 2'])
        df = pd.concat([df, df2], ignore_index=True)
    else:
        # Error handling
        df = pd.DataFrame([['Try again']], columns=['Error, Sorry!'])
    return df, history
