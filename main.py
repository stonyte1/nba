from model import Base, engine
from players import extract_players_data
from datetime import datetime, timedelta
from games import extract_games_data
from clean_save_data import clean_save_players_data, clean_save_games_data, save_teams_data

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    extract_players_data()

    yesterday_datetime = datetime.now() - timedelta(days=86)
    yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')

    extract_games_data(yesterday_date)

    clean_save_players_data()

    clean_save_games_data()
    save_teams_data()
