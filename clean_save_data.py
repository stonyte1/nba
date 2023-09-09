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

    data_no_duplicate = data.drop_duplicates(subset=data.columns.difference(['id']), keep='first')
    data_no_duplicate.to_sql('game', conn, if_exists='replace', index=False)

    cursor = conn.cursor()
    create_teams_table = '''
        CREATE TABLE teams AS
        SELECT team, SUM(points) AS total FROM game
        GROUP BY team;
    '''
    cursor.execute(create_teams_table)
    
    create_ranking_table = '''
        CREATE TABLE game_rankings AS 
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY team ORDER BY points DESC) AS ranking
        FROM game;
    '''

    cursor.execute(create_ranking_table)

    delete_table = '''
        DROP TABLE game;
    '''
    cursor.execute(delete_table)

    rename_table = '''
        ALTER TABLE game_rankings RENAME TO game;
    '''
    cursor.execute(rename_table)
    
    conn.commit()
    conn.close()

    data_no_duplicate.to_csv('games.csv')


def save_teams_data():
    conn = sqlite3.connect('players_stats.db')
    query = "SELECT * FROM teams"
    teams_data = pd.read_sql(query, conn)
    df = pd.DataFrame(teams_data)
    conn.close()

    df.to_csv('teams.csv')
