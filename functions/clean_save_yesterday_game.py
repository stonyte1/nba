import pandas as pd
import sqlite3


def clean_save_players_data():
    conn = sqlite3.connect('nba_stats.db')
    query = "SELECT * FROM player"
    players_data = pd.read_sql(query, conn)
    df = pd.DataFrame(players_data)
    conn.close()

    df.to_csv('saved_data/players.csv')
    

def clean_games_duplicates():
    conn = sqlite3.connect('nba_stats.db')

    query = "SELECT * FROM season_games"
    data = pd.read_sql(query, conn)

    data_no_duplicate = data.drop_duplicates(subset=data.columns.difference(['id']), keep='first')
    data_no_duplicate.to_sql('season_games', conn, if_exists='replace', index=False)

    conn.close()


def filter_save_latest_game():
    conn = sqlite3.connect('nba_stats.db')
    cursor = conn.cursor()

    create_latest_game_table = '''
    CREATE TABLE latest_game_stats AS
    SELECT *, 
        ROW_NUMBER() OVER (PARTITION BY team ORDER BY points DESC) AS ranking
    FROM season_games
    WHERE date = (SELECT MAX(date) FROM season_games); 
    '''
    cursor.execute(create_latest_game_table)

    conn.commit()

    select_latest_game_table = '''
    SELECT * FROM latest_game_stats 
    '''
    latest_game_data = pd.read_sql(select_latest_game_table, conn)
    latest_game_data.to_csv('saved_data/latest_game.csv')

    conn.close()


def save_teams_data():
    conn = sqlite3.connect('nba_stats.db')
    cursor = conn.cursor()

    create_teams_table = '''
        CREATE TABLE teams AS
        SELECT team, SUM(points) AS total FROM latest_game_stats
        GROUP BY team;
    '''
    cursor.execute(create_teams_table)

    conn.commit()

    select_teams_data = '''
    SELECT * FROM teams
    '''
    teams_data = pd.read_sql(select_teams_data, conn)
    teams_data.to_csv('saved_data/teams.csv')

    conn.close()


def save_players_seaosn_stats():
    conn = sqlite3.connect('nba_stats.db')

    cursor = conn.cursor()
    create_players_average_table = '''
    CREATE TABLE players_season_stats AS 
    SELECT s.id, s.points, s.rebound, s.steals, s.date, s.game_id, s.team, s.player_id, g.ranking,
        AVG(s.points) OVER (PARTITION BY s.player_id) AS season_average
    FROM season_games AS s
    JOIN latest_game_stats AS g 
    ON s.player_id = g.player_id
    WHERE g.ranking < 4
    ORDER BY s.team, g.ranking;
    '''
    cursor.execute(create_players_average_table)

    conn.commit()

    select_season_stats = '''
    SELECT * FROM players_season_stats
    '''

    season_stats = pd.read_sql(select_season_stats, conn)
    season_stats.to_csv('saved_data/season_stats.csv')
    conn.close()
