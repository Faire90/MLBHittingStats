import statsapi
import json


def final_games_dict(games_, team_id):
    try:
        with open("games.txt") as outfile:
            final_games = json.load(outfile)
        with open("games.txt", "w") as outfile:
            final_games[str(team_id)] = games_
            json.dump(final_games, outfile)
    except FileNotFoundError as err:
        print(f"{err}. Creating games.txt file.")
        with open("games.txt", "w") as outfile:
            final_games = {team_id: games_}
            json.dump(final_games, outfile)


def get_all_regular_games(team_ids, start_year=2021, end_year=2021):
    """This function creates a JSON file of all regular season game ids between a given start and end date for a given
    list of teams.  The function uses a while loop because the 'schedule' method from statsapi cannot retrieve more
    than one season at a time.  It also avoids duplicate game entries by only appending the game id for the home team.
    Otherwise, there would be two of each game."""
    games = []
    while start_year <= end_year:
        for team in team_ids:
            try:
                schedule_result = statsapi.schedule(team=team, start_date=f'03/26/{start_year}',
                                                    end_date=f'11/01/{end_year}')
            except requests.exceptions.HTTPError as err:
                print(err)
                final_games_dict(games, team)
            for i, game in enumerate(schedule_result):
                if game['game_type'] == 'R':
                    games.append(game['game_id'])
            final_games_dict(games, team)
        start_year += 1


def Retrieve_Box_Scores(team_id):
    with open('games.txt') as games_file:
        games = json.load(games_file)
    box_scores = []
    for game in games[str(team_id)]:
        try:
            box_score = statsapi.boxscore_data(game, timecode=None)
            box_scores.append(box_score)
            print(f"Appending box scores from {game}.")
        except KeyError as err:
            print(f"Keyerror: {err} in {game}. Skipping {game}")
    with open('boxscores.txt', 'w') as boxscores:
        json.dump(box_scores, boxscores)


def Retrieve_Player_Data(player_id):
    try:
        player_data = statsapi.player_stat_data(player_id)
        #player_stats.append(player_data)
        print(f"Appending player data for {player_id}.")
    except KeyError as err:
        print(f"Keyerror: {err} Skipping {player_id}")
    with open('playerdata.txt', 'w') as playerstats:
        json.dump(player_data, playerstats)


if __name__ == '__main__':
    get_all_regular_games([136])
    Retrieve_Box_Scores(136)
    # Retrieve_Player_Data(571745)
