# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import csv
import pandas as pd

class ActionListNames(Action):

    def name(self) -> Text:
        return "action_list_names"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            #df = pd.read_csv('FinalProject/data/STDSDatabase.csv')
            df = pd.read_csv('STDSDatabase.csv')

            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
            
            return []
