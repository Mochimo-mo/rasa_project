# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import requests
from typing import Dict, Any, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class action_get_leaguePosition(Action):
    def name(self) -> Text:
        return "action_get_leaguePosition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the team name from the user input
        team = tracker.get_slot("team")
        # Define the API endpoint and parameters
        url = f"https://v3.football.api-sports.io/teams?name={team}"
        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            "x-rapidapi-key": "dbab84843ad7a3bab37bcf7d742a89da"}

        # Make a GET request to the API
        response = requests.get(url, headers=headers)
        # Get the JSON data from the response
        data = response.json()
        # Extract the league position and number of games played
        team_id = data['response'][0]['team']['id']
        print(team_id)

        league_url = f"https://v3.football.api-sports.io/leagues?team={team_id}"
        league_response = requests.get(league_url, headers=headers)
        data_league = league_response.json()
        print(data_league)
        league_id = data_league['response'][0]['league']['id']
        league_name = data_league['response'][0]['league']['name']
        for season in data_league['response'][0]['seasons']:
            if season['coverage']['standings']['2023']:
                standing_url = f"https://v3.football.api-sports.io/standings?league=39&season=2019"
                standing_response = requests.get(standing_url, headers=headers)
                data_standing = standing_response.json()
                print(data_standing)
                for team in data_standing['response'][0]['league']['standings'][0]:
                    if team['team']['id'] == team_id:
                        position = team['rank']
                        print(f"Team position: {position}")
                team_position = position
                # Send the information back to the user
                message = f"They are currently in {team_position}th place in {league_name} League."
                dispatcher.utter_message(message)
            else:
                message = f"They currently have no position for this season."
                dispatcher.utter_message(message)
        # events = [
        #     SlotSet("league_name", league_name),
        #     SlotSet("league_position", rank)
        # ]

        # return [SlotSet("league_position", events)]
        return [SlotSet("leaguePosition", team_position)]

class action_get_manager(Action):
    def name(self) -> Text:
        return "action_get_manager"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the team name from the user input
        team = tracker.get_slot("team")
        # Define the API endpoint and parameters
        url = f"https://v3.football.api-sports.io/teams?name={team}"
        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            "x-rapidapi-key": "dbab84843ad7a3bab37bcf7d742a89da"}

        # Make a GET request to the API
        response = requests.get(url, headers=headers)
        # Get the JSON data from the response
        data = response.json()
        # Extract the league position and number of games played
        team_id = data['response'][0]['team']['id']
        print(team_id)

        Coaches_url = f"https://v3.football.api-sports.io/coachs?team={team_id}"
        Coaches_response = requests.get(Coaches_url, headers=headers)
        data_Coaches = Coaches_response.json()
        Coach_name = data_Coaches['response'][0]['name']

        message = f"{team}'s manager is {Coach_name}."
        dispatcher.utter_message(message)

        return [SlotSet("manager", Coach_name)]

class action_get_winLossRecord(Action):
    def name(self) -> Text:
        return "action_get_winLossRecord"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the team name from the user input
        team = tracker.get_slot("team")
        # Define the API endpoint and parameters
        url = f"https://v3.football.api-sports.io/teams?name={team}"
        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            "x-rapidapi-key": "dbab84843ad7a3bab37bcf7d742a89da"}

        # Make a GET request to the API
        response = requests.get(url, headers=headers)
        # Get the JSON data from the response
        data = response.json()
        # Extract the league position and number of games played
        team_id = data['response'][0]['team']['id']
        print(team_id)

        league_url = f"https://v3.football.api-sports.io/leagues?team={team_id}"
        league_response = requests.get(league_url, headers=headers)
        data_league = league_response.json()
        print(data_league)
        league_id = data_league['response'][0]['league']['id']

        statistic_url = f"https://v3.football.api-sports.io/teams/statistics?season=2023&team={team_id}&league={league_id}"
        statistic_response = requests.get(statistic_url, headers=headers)
        data_statistic = statistic_response.json()
        wins = data_statistic['response']['fixtures']['wins']['total']
        draws= data_statistic['response']['fixtures']['draws']['total']
        loss = data_statistic['response']['fixtures']['loss']['total']
        message = f"{wins} wins, {draws} draws and {loss} loss."
        dispatcher.utter_message(message)

        return_msg = [wins,draws,loss]

        return [SlotSet("winLossRecord", return_msg)]