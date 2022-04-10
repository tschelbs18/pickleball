import pandas as pd


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


def arrange_players(players, game_size):
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
        df2 = pd.DataFrame([[two[0]], two[1]], columns=['Team 1', 'Team 2'])
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
    return df
