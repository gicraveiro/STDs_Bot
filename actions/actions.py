# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
#from rasa_sdk import ValidationAction
#from rasa_sdk.types import DomainDict
from collections import Counter

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

class ActionTransmission(Action):

    def name(self) -> Text:
        return "action_specific_transmission"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        df = pd.read_csv('STDSDatabase.csv')
        flag = 0
        if tracker.get_slot('STD_name') is None:
            dispatcher.utter_message(text="Place here the transmission of STDs in general")
        for i, j in df.iterrows():
            #dispatcher.utter_message(text=j['Transmission'])
            if(j['Name'] == tracker.get_slot('STD_name')): # TO DO : TREATMENT FOR MISPELLING/NON EXISTENT DISEASES - I dont think its here
                specific_transmission = j['Transmission']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_transmission)
        else:
            dispatcher.utter_message(text="It seems this name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
        return []

class ActionPrevention(Action):

    def name(self) -> Text:
        return "action_specific_prevention"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        df = pd.read_csv('STDSDatabase.csv')
        flag = 0
        if tracker.get_slot('STD_name') is None:
            dispatcher.utter_message(text="Place here the prevention of STDs in general")
        for i, j in df.iterrows():
            #dispatcher.utter_message(text=j['Prevention'])
            if(j['Name'] == tracker.get_slot('STD_name')): # TO DO : TREATMENT FOR MISPELLING/NON EXISTENT DISEASES - I dont think its here
                specific_prevention = j['Prevention']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_prevention)
        else:
            dispatcher.utter_message(text="It seems this name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
        return []

class ActionDefinition(Action):

    def name(self) -> Text:
        return "action_specific_definition"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        df = pd.read_csv('STDSDatabase.csv')
        flag = 0
        if tracker.get_slot('STD_name') is None:
            dispatcher.utter_message(text="Sexually transmitted diseases (STDs), also known as sexually transmitted infections (STIs), are very common. Millions of new infections occur every year in the United States.\nSTDs pass from one person to another through vaginal, oral, and anal sex. They also can spread through intimate physical contact like heavy petting, though this is not very common.\nSTDs don’t always cause symptoms or may only cause mild symptoms. Therefore, it is possible to have an infection and not know it. That is why getting an STD test is important if you are having sex. If you receive a positive STD diagnosis, know that all are treatable with medicine and some are curable entirely.\nSTDs are preventable. If you have sex, know how to protect yourself and your sex partner(s) from STDs.")
        for i, j in df.iterrows():
            #dispatcher.utter_message(text=j['Definition'])
            if(j['Name'] == tracker.get_slot('STD_name')): # TO DO : TREATMENT FOR MISPELLING/NON EXISTENT DISEASES - I dont think its here
                specific_definition = j['Definition']
                flag = 1

        if flag == 1:
            dispatcher.utter_message(text=specific_definition)
        else:
            dispatcher.utter_message(text="It seems this name wasn't found in the database, please try spelling the STD exactly like in the list below")
            for i, j in df.iterrows():
                dispatcher.utter_message(text=j['Name'])
        return []

class ActionValidate_STD(Action):
    def name(self) -> Text:
        return "action_validate_std_name"
    
    def run(self, dispatcher: CollectingDispatcher, 
    tracker: Tracker, 
    domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

        slot_value = tracker.get_slot('STD_name')
        df = pd.read_csv('STDSDatabase.csv')

        if (slot_value is not None):
            best_match = 0
            for i, j in df.iterrows():

                std_ref = list(j['Name'].lower())
                std_real = list(slot_value.lower())

                equalChars = list((Counter(std_ref) & Counter(std_real)).elements())

                if(len(equalChars)/len(std_real) > 0.7 and ( (len(equalChars)/len(std_real)) > best_match)): # TO DO: PERFORM OFFICIAL TESTS TO FIND OUT BEST VALUE/PERFORMANCE
                    updated_slot = j['Name']
                    best_match = len(equalChars)/len(std_real)

                if best_match > 0:
                    # validation succeeded, capitalize the value of the "std_name" slot
                    print(best_match, updated_slot, "updated!")
                    return[SlotSet("STD_name", updated_slot)]
                    #return {"STD_name": updated_slot}#slot_value.capitalize()}

        # validation failed, set this slot to None
        #print("best match was given as = or less than 0")
        dispatcher.utter_message(text="This name was not recognized as one of the STDs present in the dataset. Please try spelling the STD exactly like in the list below.") # TO DO: replace it with the actual name
        #print("passed uttering back wrong name")
        for i, j in df.iterrows():
            dispatcher.utter_message(text=j['Name'])
        #print("passed list of stds")
        dispatcher.utter_message(text="TO DO: utter_list_STD_conclusion")
        #print("passed conclusion, now is setting to none")
        #return {"STD_name": None}
        return[SlotSet("STD_name", None)]
        #return []

# class ValidatePredefinedSlots(ValidationAction):
#     def validate_std_name(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher, 
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate std name value."""
#         df = pd.read_csv('STDSDatabase.csv')

#         print("we're in")

#         for i, j in df.iterrows():
#             std_ref = j['Name']
#             best_match = 0
#             #equalChars = 0
#             #for charRef,charReal in zip(std_title.lower(), slot_value.lower()):
#             #    if charRef == charReal:
#             #        equalChars += 1
#             std_ref = list(j['Name'].lower())
#             std_real = list(slot_value.lower())

#             equalChars = list((Counter(std_ref) & Counter(std_real)).elements())

#             print(equalChars)

#             if(len(equalChars)/len(std_real) > 0.6 and len(equalChars)/len(std_real) > best_match): # TO DO: PERFORM OFFICIAL TESTS TO FIND OUT BEST VALUE/PERFORMANCE
#                 updated_slot = j['Name']
#                 best_match = len(equalChars)/len(std_real)
#                 print(updated_slot, best_match)
#         #if isinstance(slot_value, str):
#         if best_match > 0:
#             # validation succeeded, capitalize the value of the "std_name" slot
#             print(best_match, updated_slot, "updated!")
#             return {"STD_name": updated_slot}#slot_value.capitalize()}
#         else:
#             # validation failed, set this slot to None
#             print("returning None")
#             return {"STD_name": None}