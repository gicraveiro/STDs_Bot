# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet #, FollowupAction
#from rasa_sdk import ValidationAction
#from rasa_sdk.types import DomainDict
from collections import Counter
#import csv
import pandas as pd
    
class ActionValidate_STD(Action): 
    def name(self) -> Text:
        return "validate_std_name"
    
    def run(self, dispatcher: CollectingDispatcher, 
    tracker: Tracker, 
    domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

        slot_value = tracker.get_slot('STD_name')
        df = pd.read_csv('data/STDSDatabase.csv')

        if (slot_value is not None):
            best_match = 0
            for i, j in df.iterrows():

                std_ref = list(j['Name'].lower())
                std_real = list(slot_value.lower())

                equalChars = list((Counter(std_ref) & Counter(std_real)).elements())

                # enough characters have to be the same + real and reference cant have a big diference of number of letters... to try to fix the pelvic inflammatory disease which matches everyone...
                if(len(equalChars)/len(std_real) > 0.7 and ( (len(equalChars)/len(std_real)) > best_match) and len(std_ref) - len(std_real) < 5): # TO DO: PERFORM OFFICIAL TESTS TO FIND OUT BEST VALUE/PERFORMANCE
                    updated_slot = j['Name']
                    best_match = len(equalChars)/len(std_real)

            if best_match > 0:
                # validation succeeded
                print(best_match, updated_slot, "updated!")
                return[SlotSet("STD_name", updated_slot)]

        #print("no std was recognized")
        return[] #SlotSet("STD_name", None)]

class ActionSetEntityNone(Action):
    def name(self) -> Text:
        return "action_set_entity_none"
    
    def run(self, dispatcher: CollectingDispatcher, 
    tracker: Tracker, 
    domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
    
        return[SlotSet("STD_name", None)]  


class ActionListNames(Action):

    def name(self) -> Text:
        return "action_list_names"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            #df = pd.read_csv('FinalProject/data/STDSDatabase.csv')
            df = pd.read_csv('data/STDSDatabase.csv')

            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
            
            return []


class ActionTransmission(Action):

    def name(self) -> Text:
        return "action_specific_transmission"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('STD_name') is None:
            dispatcher.utter_message(response="utter_transmission_STD")
            return []

        df = pd.read_csv('data/STDSDatabase.csv')
        flag = 0
        for i, j in df.iterrows():

            if(j['Name'] == tracker.get_slot('STD_name')):
                specific_transmission = j['Transmission']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_transmission)
        else:
            dispatcher.utter_message(text="It seems this name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
            dispatcher.utter_message(response="utter_list_STD_conclusion")
        return []

class ActionPrevention(Action):

    def name(self) -> Text:
        return "action_specific_prevention"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('STD_name') is None:
            dispatcher.utter_message(response="utter_prevention_STD")
            return []

        df = pd.read_csv('data/STDSDatabase.csv')
        flag = 0
        for i, j in df.iterrows():

            if(j['Name'] == tracker.get_slot('STD_name')):
                specific_prevention = j['Prevention']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_prevention)
        else:
            dispatcher.utter_message(text="It seems this name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
            dispatcher.utter_message(response="utter_list_STD_conclusion")
        return []

class ActionDefinition(Action):

    def name(self) -> Text:
        return "action_specific_definition"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('STD_name') is None:            
            dispatcher.utter_message(response="utter_definition_STD")
            return []

        df = pd.read_csv('data/STDSDatabase.csv')
        flag = 0
        for i, j in df.iterrows():

            if(j['Name'] == tracker.get_slot('STD_name')): 
                specific_definition = j['Definition']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_definition)
        else:
            dispatcher.utter_message(text="It seems this std name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
            dispatcher.utter_message(response="utter_list_STD_conclusion")
        return []

class ActionDiagnosis(Action):

    def name(self) -> Text:
        return "action_specific_diagnosis"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('STD_name') is None:
            dispatcher.utter_message(response="utter_diagnosis_STD")
            return []

        df = pd.read_csv('data/STDSDatabase.csv')
        flag = 0
        for i, j in df.iterrows():

            if(j['Name'] == tracker.get_slot('STD_name')):
                specific_diagnosis = j['Diagnosis']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_diagnosis)
        else:
            dispatcher.utter_message(text="It seems this name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
            dispatcher.utter_message(response="utter_list_STD_conclusion")
        return []

class ActionSymptoms(Action):

    def name(self) -> Text:
        return "action_specific_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('STD_name') is None:
            dispatcher.utter_message(response="utter_symptoms_STD")
            return []

        df = pd.read_csv('data/STDSDatabase.csv')
        flag = 0
        for i, j in df.iterrows():

            if(j['Name'] == tracker.get_slot('STD_name')):
                specific_symptoms = j['Symptoms']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_symptoms)
        else:
            dispatcher.utter_message(text="It seems this name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
            dispatcher.utter_message(response="utter_list_STD_conclusion")
        return []

class ActionTreatment(Action):

    def name(self) -> Text:
        return "action_specific_treatment"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('STD_name') is None:
            dispatcher.utter_message(response="utter_treatment_STD")
            return []

        df = pd.read_csv('data/STDSDatabase.csv')
        flag = 0
        for i, j in df.iterrows():

            if(j['Name'] == tracker.get_slot('STD_name')):
                specific_treatment = j['Treatment']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_treatment)
        else:
            dispatcher.utter_message(text="It seems this name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
            dispatcher.utter_message(response="utter_list_STD_conclusion")
        return []

class ActionConsequences(Action):

    def name(self) -> Text:
        return "action_specific_consequences"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('STD_name') is None:
            dispatcher.utter_message(response="utter_consequences_STD")
            return []

        df = pd.read_csv('data/STDSDatabase.csv')
        flag = 0
        for i, j in df.iterrows():

            if(j['Name'] == tracker.get_slot('STD_name')):
                specific_consequences = j['Consequences']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_consequences)
        else:
            dispatcher.utter_message(text="It seems this name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
            dispatcher.utter_message(response="utter_list_STD_conclusion")
        return []

