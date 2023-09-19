from functions.model import Base, engine
from functions.players import extract_players_data
from functions.games import extract_games_data
from functions.clean_save_yesterday_game import clean_save_players_data, clean_games_duplicates, filter_save_latest_game, save_teams_data, save_players_seaosn_stats


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    extract_players_data()
    clean_save_players_data()

    extract_games_data()
    clean_games_duplicates()
    filter_save_latest_game()

    # save_teams_data()

    save_players_seaosn_stats()
