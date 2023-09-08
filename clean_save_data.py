import pandas as pd
import sqlite3


def clean_save_players_data():
    conn = sqlite3.connect('players_stats.db')
    query = "SELECT * FROM player"
    players_data = pd.read_sql(query, conn)
    df = pd.DataFrame(players_data)
    conn.close()

    df.to_csv('players.csv')


def clean_save_games_data():
    conn = sqlite3.connect('players_stats.db')
    query = "SELECT * FROM game"
    data = pd.read_sql(query, conn)

    df = pd.DataFrame(data)

    df_no_duplicate = df.drop_duplicates(subset=df.columns.difference(['id']), keep='first')
    df_no_duplicate.to_sql('game', conn, if_exists='replace', index=False)

    query = '''
        CREATE TABLE teams AS
        SELECT team, SUM(points) AS total FROM game
        GROUP BY team;

        CREATE TABLE game_rankings AS 
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY team ORDER BY points DESC) AS ranking
        FROM game;

        DROP TABLE game;

        ALTER TABLE game_rankings RENAME TO game;
    '''
    proccesed_data = pd.read_sql(query, conn)

    conn.close()

    proccesed_data.to_csv('games.csv')


def save_teams_data():
    conn = sqlite3.connect('players_stats.db')
    query = "SELECT * FROM teams"
    teams_data = pd.read_sql(query, conn)
    df = pd.DataFrame(teams_data)
    conn.close()

    df.to_csv('teams.csv')
