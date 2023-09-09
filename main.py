from functions.model import Base, engine
from functions.players import extract_players_data
from datetime import datetime, timedelta
from functions.games import extract_games_data
from functions.clean_save_data import clean_save_players_data, clean_save_games_data, save_teams_data

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    extract_players_data()

    yesterday_datetime = datetime.now() - timedelta(days=90)
    yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')

    extract_games_data(yesterday_date)

    clean_save_players_data()

    clean_save_games_data()
    save_teams_data()
